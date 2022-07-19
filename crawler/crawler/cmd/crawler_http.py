import hydra
from omegaconf import DictConfig, OmegaConf
from crawler.internal.config.config_pb2 import Bootstrap
from crawler.cmd.wire_gen import wire_stock_info
from crawler.internal.server.http import NewHTTPServer
from google.protobuf.json_format import ParseDict, MessageToJson


@hydra.main(config_path='../config', config_name='config.yaml')
def start_http(cfg: DictConfig) -> None:

    print(OmegaConf.to_yaml(cfg))
    cfg = ParseDict(cfg, Bootstrap())
    print(MessageToJson(cfg))
    _, stock_info_service = wire_stock_info(cfg)
    http_srv = NewHTTPServer(cfg.server, stock_info_service)
    app = http_srv.app
    app.run(host=http_srv.endpoint.hostname, port=http_srv.endpoint.port,
            debug=True)


if __name__ == '__main__':
    start_http()
