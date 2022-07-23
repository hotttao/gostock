
import grpc

from typing import List
from concurrent import futures
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2_grpc
from pykit.errors import Error
import multiprocessing as mp
from pykit.transport import IServer
from pykit.middleware import Middleware
from pykit.transport.grpc.interceptor import MiddlewareInterceptor
from pykit.utils import host


class Server(IServer):
    endpoint = None

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

        self.stop_event = mp.Event()
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

        self.endpoint = host.parse_address(self.address, scheme='grpc')
        return self.endpoint

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
        print("grpc started")
        self.stop_event.wait()
        print('grpc server get stop signal')
        self.server.stop(grace=60)
        # self.server.wait_for_termination()
        print('grpc server exited successfully')

    def stop(self):
        print("grpc will stop")
        self.stop_event.set()
        # self.server.stop(grace=None)
        print("grpc stop successfully")

    def server_interceptor(self):
        """
        返回包含自定义中间件的 grpc unary_interceptor
        """
        return MiddlewareInterceptor(middlewares=self.middleware)
