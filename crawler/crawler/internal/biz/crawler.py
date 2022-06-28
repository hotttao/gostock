from abc import ABCMeta, abstractmethod
from pandas import DataFrame


class StockInfo:
    def __init__(self, name):
        pass


class IStockRepo(metaclass=ABCMeta):
    """

    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.
    """

    @abstractmethod
    def get_stock_info(self, id: int):
        pass

    @abstractmethod
    def upinsert_stock_list(self, df_stock_basic):
        pass


class ICrawlerRepo(metaclass=ABCMeta):
    """
    股票数据获取的接口
    """
    @abstractmethod
    def get_stock_list(self) -> DataFrame:
        pass


class CrawlerUsecase:
    def __init__(self, stock_repo: IStockRepo, crawler_repo: ICrawlerRepo):
        self.stock_repo = stock_repo
        self.crawler_repo = crawler_repo

    def update_stock_list(self):
        df_stock_basic = self.crawler_repo.get_stock_list()
        self.stock_repo.upinsert_stock_list(df_stock_basic)
        return df_stock_basic
