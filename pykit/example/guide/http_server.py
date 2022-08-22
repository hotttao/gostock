
import hydra
from omegaconf import DictConfig, OmegaConf
import helloworld_pb2
import helloworld_pb2_grpc

from pykit.app import PyKit
from pykit.transport import http
from pykit.middleware import recovery
# from pykit.contrib.registry.consul import ConsulClient

class GreeterImp(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        reply = helloworld_pb2.HelloReply(message=f'hello {request.name}')
        return reply


def new_http_server(c: DictConfig,
                    greeter_server: helloworld_pb2_grpc.GreeterServicer) -> http.Server:
    middlewares = [
        recovery.Recovery()
    ]
    srv = http.Server(c.http.addr, middlewares=middlewares)
    stock_v1.RegisterStockInfoServiceHTTPServer(srv, greeter_server)
    # srv.Handle("/metrics", promhttp.Handler())
    # v1.RegisterGreeterHTTPServer(srv, greeter)
    # evaluate_v2.RegisterIncomeHTTPServer(srv, income)
    # stock_v1.RegisterStockInfoServiceHTTPServer(srv, stock)
    return srv


@hydra.main(config_path='./config', config_name='config.yaml')
def start_http_server(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    # 2. 初始化 grpc server
    greeter_service = GreeterImp()
    http_srv = new_http_server(cfg.server, greeter_service)

    # 3. 启动服务
    # consul = ConsulClient(host=cfg.connection.consul.host,
    #                       port=cfg.connection.consul.port)
    # registrar = ConsulImp(client=consul)
    app = PyKit(id='1111', name='crawler', version='1.0.1',
                servers=[http_srv])
    app.run()
