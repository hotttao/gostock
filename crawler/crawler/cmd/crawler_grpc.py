import hydra
from omegaconf import DictConfig, OmegaConf
from crawler.internal.config.config_pb2 import Bootstrap
from crawler.cmd.wire_gen import wire_stock_info
from crawler.internal.server.grpc import NewGrpcServer
from google.protobuf.json_format import ParseDict, MessageToJson


@hydra.main(config_path='../config', config_name='config.yaml')
def start_grpc(cfg: DictConfig) -> None:

    print(OmegaConf.to_yaml(cfg))
    cfg = ParseDict(cfg, Bootstrap())
    print(MessageToJson(cfg))
    _, stock_info_service = wire_stock_info(cfg)
    grpc_srv = NewGrpcServer(cfg.server, stock_info_service)
    grpc_srv.start()


if __name__ == '__main__':
    start_grpc()
