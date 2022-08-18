
import flask
from typing import List, Callable
from pykit.utils import host
import multiprocessing as mp
from pykit.transport import http, IServer
import cherrypy
# from waitress import create_server


class Server(IServer):
    endpoint = None

    def __init__(self, address, middlewares: List[Callable] = None,
                 encoder_error: Callable = None, encoder_response: Callable = None) -> None:
        self.app = flask.Flask('test')
        self.err = None  # error
        self.network = None  # string
        self.address = address  # string
        self.endpoint = None
        self.timeout = None  # time.Duration
        self.filters = []  # []FilterFunc
        self.middlewares = middlewares or []  # []middleware.Middleware
        self.dec = []  # DecodeRequestFunc
        # EncodeResponseFunc
        self.encoder_response = encoder_response or http.default_response_encoder
        self.encoder_error = encoder_error or http.default_error_encoder  # EncodeErrorFunc
        self.init()

        self._server = None
        self.stop_event = mp.Event()

    def start(self):
        # self.app.run(host=self.endpoint.hostname, port=self.endpoint.port,
        #              debug=True)
        # self._server = create_server(self.app, listen=self.address)
        # self._server.run()

        cherrypy.tree.graft(self.app, '/')
        cherrypy.config.update({'server.socket_host': self.endpoint.hostname,
                                'server.socket_port': self.endpoint.port,
                                'engine.autoreload.on': False,
                                })
        cherrypy.engine.start()
        # TODO: self.stop_event.wait() 添加后，进程无法退出
        # self.stop_event.wait()
        print('http server start return')

    def stop(self):
        print("http will stop")
        self.stop_event.set()
        cherrypy.engine.exit()
        print("http stoped")

        # if self._server:
        # self._server.close()

    def init(self):
        self.listen_and_endpoint()

    def listen_and_endpoint(self):
        """
        """
        self.endpoint = host.parse_address(self.address, scheme='http')
        return self.endpoint

    def router(self, prefix=''):
        return http.Router(self, prefix=prefix)

    def handler(self, method: str, url: str, h: Callable):
        # self.app.route()
        self.app.add_url_rule(rule=url, view_func=h, methods=[method])
