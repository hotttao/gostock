
import grpc
from urllib import parse
from typing import List
from concurrent import futures
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2_grpc
from pykit.error import Error
from pykit.middleware import Middleware
from pykit.transport.grpc.interceptor import MiddlewareInterceptor


class Server:
    def __init__(self, address: str, network: str = 'tcp', error: Error = None,
                 middleware: List[Middleware] = None, interceptor: grpc.ServerInterceptor = None,
                 ):
        self.error = error
        self.address = address
        self.network = network or 'tcp'

        # endpoint * url.URL
        # timeout    time.Duration
        self.middleware = middleware or []
        self.interceptor = interceptor or []
        self.health = health.HealthServicer()
        self.metadata = None
        self.server = None

        self.init()

    def init(self):
        self.listen_and_endpoint()
        interceptors = [self.server_interceptor()]
        if self.interceptor:
            interceptors.extend(self.interceptor)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                                  interceptors=interceptors)
        health_pb2_grpc.add_HealthServicer_to_server(server=self.server, servicer=self.health)

    def listen_and_endpoint(self):
        """
        """

        # url_obj = parse.urlparse(self.address)
        # print(url_obj)
        self.endpoint = parse.ParseResult(scheme='grpc', netloc=self.address, query='isSecure=false',
                                          path='', params='', fragment='')
        return

    def register(self, register_func, servicer):
        """_summary_

        Args:
            register_func (_type_): _description_
            servicer (_type_): _description_
        """
        register_func(server=self.server, servicer=servicer)

    def start(self):
        """

        """
        # print(self.address, self.endpoint)
        self.server.add_insecure_port(self.endpoint.netloc)
        self.server.start()
        self.server.wait_for_termination()

    def stop(self):
        pass

    def server_interceptor(self):
        """
        返回包含自定义中间件的 grpc unary_interceptor
        """
        return MiddlewareInterceptor(middlewares=self.middleware)
