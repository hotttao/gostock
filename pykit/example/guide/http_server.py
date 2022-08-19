
import hydra
from omegaconf import DictConfig, OmegaConf
from crawler.internal.server.grpc import NewGrpcServer
from google.protobuf.json_format import ParseDict, MessageToJson

from pykit.app import PyKit
from pykit.contrib.registry.consul import ConsulClient


@hydra.main(config_path='./config', config_name='config.yaml')
def start_http_server():
    print(OmegaConf.to_yaml(cfg))
    cfg = ParseDict(cfg, Bootstrap())
    print(MessageToJson(cfg))
    _, stock_info_service = wire_stock_info(cfg)
    http_srv = NewHTTPServer(cfg.server, stock_info_service)

    # 3. 启动服务
    consul = ConsulClient(host=cfg.connection.consul.host, port=cfg.connection.consul.port)
    registrar = ConsulImp(client=consul)
    app = PyKit(id='1111', name='crawler', version='1.0.1',
                servers=[http_srv], registrar=registrar)
    app.run()
    