
import grpc

from typing import List
from concurrent import futures
import multiprocessing as mp
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection
from pykit.transport import IServer
from pykit.middleware import Middleware
from pykit.transport.grpc.interceptor import MiddlewareInterceptor
from pykit.utils import host


class Server(IServer):
    endpoint = None

    def __init__(self, address: str, network: str = 'tcp',
                 middleware: List[Middleware] = None, interceptor: grpc.ServerInterceptor = None,
                 ):
        self.address = address
        self.network = network or 'tcp'
        self.middleware = middleware or []
        self.interceptor = interceptor or []

        # 所有注册的 grpc server
        self._services_descriptor = {}
        self.stop_event = mp.Event()
        self.init()

    def init(self):
        self.metadata = None

        self.listen_and_endpoint()
        interceptors = [self.server_interceptor()]
        if self.interceptor:
            interceptors.extend(self.interceptor)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                                  interceptors=interceptors)
        # 添加健康检测服务
        self.health = health.HealthServicer()
        self.health.set('', health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(server=self.server, servicer=self.health)

    def add_reflection_servicer(self):
        """添加 grpc reflection
        """
        for name in self._services_descriptor.keys():
            service_name = (
                name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(service_name, self.server)

    def listen_and_endpoint(self):
        """地址解析
        """
        self.endpoint = host.parse_address(self.address, scheme='grpc')
        return self.endpoint

    def register(self, descriptor, register_func, servicer):
        """_summary_

        Args:
            register_func (_type_): _description_
            servicer (_type_): _description_
        """
        self._services_descriptor[descriptor.full_name] = descriptor
        register_func(server=self.server, servicer=servicer)

    def start(self):
        """启动服务
        """
        self.add_reflection_servicer()
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
