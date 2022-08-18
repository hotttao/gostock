import grpc
import copy
from typing import Dict, List
from pykit.transport.grpc.interceptor import ClientInterceptorWrapt
from pykit.middleware import Middleware
from grpc_interceptor import ClientInterceptor


class Client:
    def __init__(self, endpoint: str, timeout: int = 10, discovery=None,
                 middleware: List[Middleware] = None,
                 interceptors: List[ClientInterceptor] = None,
                 balancer_name: str = 'wrr', grpc_options: Dict = None):
        self.endpoint = endpoint
        self.timeout = timeout
        self.middleware = middleware or []
        self.discovery = discovery
        self.ints = interceptors or []
        self.balancer_name = balancer_name
        self.grpc_options = grpc_options or {}
        # filters[]selector.Filter

    def dail(self):
        interceptors = copy.deepcopy(self.ints)
        if self.middleware:
            interceptors.append(ClientInterceptorWrapt(self.middleware))
        channel = grpc.insecure_channel(self.endpoint)
        channel = grpc.intercept_channel(channel, *interceptors)
        return channel

    def do_discovery(self):
        """处理服务发现的逻辑
        """
        pass
