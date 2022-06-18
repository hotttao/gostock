import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(config_path='../config', config_name='config.yaml')
def start_crawler(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == '__main__':
    start_crawler()
