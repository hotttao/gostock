
from typing import Dict
import hydra
from omegaconf import DictConfig, OmegaConf
import helloworld_pb2
import helloworld_pb2_grpc
from pykit.app import PyKit
from pykit.transport import grpc
from pykit.middleware import recovery
# from pykit.contrib.registry.consul import ConsulClient


class GreeterImp(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        reply = helloworld_pb2.HelloReply(message=f'hello {request.name}')
        return reply


def new_grpc_server(c: Dict, greeter_server: helloworld_pb2_grpc.GreeterServicer) -> grpc.Server:
    """初始化 grpc server

    Args:
        c (config_pb2.Server): _description_
        stock_info (stock_v1.IStockInfoServiceHTTPServer): _description_

    Returns:
        grpc.Server: _description_
    """
    # print(c.grpc, stock_info)
    middleware = [
        recovery.Recovery()
    ]
    server = grpc.Server(address=c.grpc.addr, network=c.grpc.network,
                         middleware=middleware)
    server.register(descriptor=helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'],
                    register_func=helloworld_pb2_grpc.add_GreeterServicer_to_server,
                    servicer=greeter_server)
    return server


@hydra.main(config_path='./config', config_name='config.yaml')
def start_grpc_server(cfg: DictConfig) -> None:
    # 1. 准备配置文件
    print(OmegaConf.to_yaml(cfg.server))

    # 2. 初始化 grpc server
    greeter_service = GreeterImp()
    grpc_srv = new_grpc_server(cfg.server, greeter_service)

    # 3. 启动服务
    # consul = ConsulClient(host=cfg.connection.consul.host,
    #                       port=cfg.connection.consul.port)
    app = PyKit(id='1111', name='crawler', version='1.0.1',
                servers=[grpc_srv])
    app.run()


if __name__ == '__main__':
    start_grpc_server()
