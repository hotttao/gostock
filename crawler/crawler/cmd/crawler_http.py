import hydra
from omegaconf import DictConfig, OmegaConf
from crawler.internal.config.config_pb2 import Bootstrap
from crawler.cmd.wire_gen import wire_stock_info
from crawler.internal.server.http import NewHTTPServer
from google.protobuf.json_format import ParseDict, MessageToJson
from pykit.app import PyKit
from pykit.contrib.registry.consul import ConsulClient


@hydra.main(config_path='../config', config_name='config.yaml')
def start_http(cfg: DictConfig) -> None:

    print(OmegaConf.to_yaml(cfg))
    cfg = ParseDict(cfg, Bootstrap())
    print(MessageToJson(cfg))
    _, stock_info_service = wire_stock_info(cfg)
    http_srv = NewHTTPServer(cfg.server, stock_info_service)

    # 3. 启动服务
    consul = ConsulClient(host=cfg.connection.consul.host, port=cfg.connection.consul.port)
    app = PyKit(id='1111', name='crawler', version='1.0.1',
                servers=[http_srv], registrar=consul)
    app.run()


if __name__ == '__main__':
    start_http()
