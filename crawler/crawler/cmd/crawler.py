import hydra
from omegaconf import DictConfig, OmegaConf
from crawler.internal.config.config_pb2 import Bootstrap
from crawler.cmd.wire_gen import wire_app
from google.protobuf.json_format import ParseDict, MessageToJson


def new_app(config: Bootstrap):
    pass


@hydra.main(config_path='../config', config_name='config.yaml')
def start_crawler(cfg: DictConfig) -> None:

    print(OmegaConf.to_yaml(cfg))
    cfg = ParseDict(cfg, Bootstrap())
    print(MessageToJson(cfg))
    crawler = wire_app(cfg)
    df = crawler.update_stock_list()
    print(df)


if __name__ == '__main__':
    start_crawler()
