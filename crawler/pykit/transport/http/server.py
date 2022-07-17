
import flask
from typing import List, Callable
from urllib import parse
from pykit.transport import http


class Server:
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

    def init(self):
        self.listen_and_endpoint()

    def listen_and_endpoint(self):
        """
        """
        address = self.address
        if '//' not in self.address:
            address = f'http://{self.address}'
        url_parsed = parse.urlparse(address)
        self.endpoint = parse.ParseResult(scheme='grpc', netloc=url_parsed.netloc, query='isSecure=false',
                                          path='', params='', fragment='')
        return

    def router(self, prefix=''):
        return http.Router(self, prefix=prefix)

    def handler(self, method: str, url: str, h: Callable):
        # self.app.route()
        self.app.add_url_rule(rule=url, view_func=h, methods=[method])


class Client:
    pass
