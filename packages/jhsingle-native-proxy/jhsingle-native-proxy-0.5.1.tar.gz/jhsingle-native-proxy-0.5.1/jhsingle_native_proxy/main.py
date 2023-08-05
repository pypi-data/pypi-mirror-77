from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado.web import Application, RequestHandler
from tornado.log import app_log
from asyncio import ensure_future
import click
import re
import os
import logging

from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub import __version__ as __jh_version__

from .proxyhandlers import _make_serverproxy_handler, AddSlashHandler
from .util import url_path_join
from .activity import start_keep_alive, configure_http_client
from .gitwrapper import GitWrapper


def patch_default_headers():
    if hasattr(RequestHandler, '_orig_set_default_headers'):
        return
    RequestHandler._orig_set_default_headers = RequestHandler.set_default_headers

    def set_jupyterhub_header(self):
        self._orig_set_default_headers()
        self.set_header('X-JupyterHub-Version', __jh_version__)

    RequestHandler.set_default_headers = set_jupyterhub_header


def make_app(destport, prefix, command, presentation_path, authtype, request_timeout, ready_check_path, repo, repobranch, repofolder, conda_env_name, debug):

    presentation_basename = ''
    presentation_dirname = ''

    if presentation_path:
        presentation_basename = os.path.basename(presentation_path)
        presentation_dirname = os.path.dirname(presentation_path)

    patch_default_headers()

    gitwrapper = None
    if repo != '':
        gitwrapper = GitWrapper(repo, repobranch, repofolder)
        ensure_future(gitwrapper.start_pull())

    if conda_env_name != '':
        from .conda_runner import get_conda_prefix_and_env

        conda_prefix, env_path = get_conda_prefix_and_env(conda_env_name)
        
        command = ['python3', '-m', 'jhsingle_native_proxy.conda_runner', conda_prefix, env_path] + command

    proxy_handler = _make_serverproxy_handler('mainprocess', command, {}, 10, False, destport, ready_check_path, gitwrapper, {})

    return Application([
        (
            r"^"+re.escape(prefix)+r"$",
            AddSlashHandler
        ),
        (
            url_path_join(prefix, 'oauth_callback'),
            HubOAuthCallbackHandler,
        ),
        (
            r"^"+re.escape(prefix)+r"/(.*)",
            proxy_handler,
            dict(state={}, authtype=authtype)
        )
    ],
    debug=debug,
    cookie_secret=os.urandom(32),
    user=os.environ.get('JUPYTERHUB_USER') or '',
    group=os.environ.get('JUPYTERHUB_GROUP') or '',
    anyone=os.environ.get('JUPYTERHUB_ANYONE') or '',
    base_url=prefix, # This is a confusing name, sorry
    presentation_path=presentation_path,
    presentation_basename=presentation_basename,
    presentation_dirname=presentation_dirname,
    request_timeout=request_timeout
    )

def get_ssl_options():
    ssl_options = {}
    keyfile = os.environ.get('JUPYTERHUB_SSL_KEYFILE') or ''
    certfile = os.environ.get('JUPYTERHUB_SSL_CERTFILE') or ''
    client_ca = os.environ.get('JUPYTERHUB_SSL_CLIENT_CA') or ''

    if keyfile:
        ssl_options['keyfile'] = keyfile

    if certfile:
        ssl_options['certfile'] = certfile

    if client_ca:
        ssl_options['ca_certs'] = client_ca

    if not ssl_options:
        # None indicates no SSL config
        ssl_options = None
    else:
        # SSL may be missing, so only import it if it's to be used
        import ssl
        # PROTOCOL_TLS selects the highest ssl/tls protocol version that both the client and
        # server support. When PROTOCOL_TLS is not available use PROTOCOL_SSLv23.
        # PROTOCOL_TLS is new in version 2.7.13, 3.5.3 and 3.6
        ssl_options.setdefault(
            'ssl_version',
            getattr(ssl, 'PROTOCOL_TLS', ssl.PROTOCOL_SSLv23)
        )
        if ssl_options.get('ca_certs', False):
            ssl_options.setdefault('cert_reqs', ssl.CERT_REQUIRED)

    return ssl_options

@click.command()
@click.option('--port', default=8888, help='port for the proxy server to listen on')
@click.option('--destport', default=0, help='port that the webapp should end up running on; default 0 to be assigned a random free port')
@click.option('--ip', default=None, help='Address to listen on')
@click.option('--presentation-path', default='', help='presentation_path substitution variable')
@click.option('--debug/--no-debug', default=False, help='To display debug level logs')
@click.option('--authtype', type=click.Choice(['oauth', 'none'], case_sensitive=True), default='oauth')
@click.option('--request-timeout', default=300, type=click.INT, help='timeout of proxy http calls to subprocess in seconds (default 300)')
@click.option('--last-activity-interval', default=300, type=click.INT, help='frequency to notify hub that dashboard is still running in seconds (default 300), 0 for never')
@click.option('--force-alive/--no-force-alive', default=True, help='Always report that there has been activity (force keep alive) - only happens if last-activity-interval > 0')
@click.option('--ready-check-path', default='/', help='URL path to poll for readiness (default /)')
@click.option('--repo', default='', help="Git repo to pull before running webapp subprocess")
@click.option('--repobranch', default='master', help="Branch to checkout (if --repo provided)")
@click.option('--repofolder', default='.', help="Relative folder to hold git repo contents (if --repo provided)")
@click.option('--conda-env', default='', help="Name of conda env to activate before running process")
@click.option('--allow-root/--no-allow-root', default=True, help='Currently ignored - present to avoid error if this flag is usually passed to singleuser notebook')
@click.argument('command', nargs=-1, required=True)
def run(port, destport, ip, presentation_path, debug, authtype, request_timeout, last_activity_interval, force_alive, ready_check_path, 
        repo, repobranch, repofolder, conda_env, allow_root, command):

    if debug:
        print('Setting debug')
        app_log.setLevel(logging.DEBUG)

    prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')

    if len(prefix) > 0 and prefix[-1] == '/':
        prefix = prefix[:-1]

    configure_http_client()

    app = make_app(destport, prefix, list(command), presentation_path, authtype, request_timeout, ready_check_path, repo, repobranch, repofolder, conda_env, debug)

    ssl_options = get_ssl_options()

    http_server = HTTPServer(app, ssl_options=ssl_options, xheaders=True)

    http_server.listen(port, ip)

    print("Starting jhsingle-native-proxy server on address {} port {}, proxying to port {}".format(ip, port, destport))
    print("URL Prefix: {}".format(prefix))
    print("Auth Type: {}".format(authtype))
    print("Command: {}".format(command))

    if last_activity_interval > 0:
        start_keep_alive(last_activity_interval, force_alive, app.settings)

    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()
