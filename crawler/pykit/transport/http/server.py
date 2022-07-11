
import flask
from urllib import parse
from typing import Callable, Any
from flask import request


class Server:
    def __init__(self, address) -> None:
        self.app = flask.Flask('test')
        self.err = None  # error
        self.network = None  # string
        self.address = address  # string
        self.endpoint = None
        self.timeout = None  # time.Duration
        self.filters = []  # []FilterFunc
        self.ms = []  # []middleware.Middleware
        self.dec = []  # DecodeRequestFunc
        self.enc = None  # EncodeResponseFunc
        self.ene = None  # EncodeErrorFunc
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

    def handler(self, method: str, url: str, h: Callable[[request], Any]):
        # self.app.route()
        self.app.add_url_rule(rule=url, view_func=h, methods=[method])

    def get(self, url: str, h: Callable[[request], Any]):
        self.handler('GET', url, h)

    def post(self, url: str, h: Callable[[request], Any]):
        self.handler('POST', url, h)


class Client:
    pass
