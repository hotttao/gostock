from typing import List
from urllib import urlparse
from pykit.selector import Selector
from pykit.selector import wrr
from pykit.registry import Discovery
from pykit.middleware import Middleware
from pykit.transport.http import resolver


def encode_url(url):
    pass


class Client:
    def __init__(self, endpoint: str, user_agent: str = '', decoder=None, encoder=None, error_decoder=None,
                 timeout: int = 2, block: bool = False, transport=None, selector: Selector = None,
                 discovery: Discovery = None, middlewares: List[Middleware] = None):
        self.err = None  # error
        self.timeout = timeout  # time.Duration
        self.endpoint = endpoint
        self.user_agent = user_agent

        self.decoder = decoder  # DecodeResponseFunc
        self.encoder = encoder  # EncodeRequestFunc
        self.error_decoder = error_decoder  # DecodeErrorFunc

        self.selector = selector or wrr.NewWrr()  # selector.Selector
        self.discovery = discovery  # registry.Discovery
        self.middlewares = middlewares or []  # []middleware.Middleware

        self.block = block

        self.target = urlparse(endpoint)  # Target
        self.r = resolver.new_resolver()       # resolver

        self.transport = transport
        self.cc = None      # *http.Client
