import os
from typing import Callable, List
from flask import request
from pykit.transport import http
from pykit.middleware import Chain


class Router:
    def __init__(self, srv: http.Server, prefix: str, filters: List[Callable] = None):
        self.srv = srv
        self.prefix = prefix
        self.filters = filters

    def handler(self, method: str, url: str, h: Callable):
        """
        生成注册到 web 框架的路由
        """
        def _router_hanlder(**kwargs):
            ctx = http.Context(request=request, url_params=kwargs)
            try:
                return h(ctx)
            except Exception as e:
                return self.srv.error_encoder(ctx, e)
        self.srv.handler(method=method, url=os.path.join(self.prefix, url), h=_router_hanlder)

    def get(self, url: str, h: Callable):
        self.handler('GET', url, h)

    def post(self, url: str, h: Callable):
        self.handler('POST', url, h)

    def middleware(self, handler: Callable):
        return Chain(self.srv.middlewares)(handler)
