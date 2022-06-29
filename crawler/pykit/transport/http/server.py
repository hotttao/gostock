
import flask
from typing import Callable, Any
from flask import request


class Server:
    def __init__(self) -> None:
        self.app = flask.Flask()
        self.err = None  # error
        self.network = None  # string
        self.address = None  # string
        self.timeout = None  # time.Duration
        self.filters = []  # []FilterFunc
        self.ms = []  # []middleware.Middleware
        self.dec = []  # DecodeRequestFunc
        self.enc = None  # EncodeResponseFunc
        self.ene = None  # EncodeErrorFunc

    def handler(self, method: str, url: str, h: Callable[[request], Any]):
        # self.app.route()
        self.app.add_url_rule(rule=url, view_func=h, methods=[method])

    def get(self, url: str, h: Callable[[request], Any]):
        self.handler('GET', url, h)

    def post(self, url: str, h: Callable[[request], Any]):
        self.handler('POST', url, h)


class Client:
    pass
