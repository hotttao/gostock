
import flask
from typing import List, Callable
from pykit.utils import host
import multiprocessing as mp
from pykit.transport import http, IServer


class Server(IServer):
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
        
        self.stop_event = mp.Event()

    def start(self):
        self.app.run(host=self.endpoint.hostname, port=self.endpoint.port,
                     debug=True)
        print("http server exited")

    def stop(self):
        func = flask.request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        print("http will stop")
        func()

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


class Client:
    pass
