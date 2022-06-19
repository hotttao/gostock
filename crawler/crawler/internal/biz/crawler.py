from abc import ABCMeta, abstractmethod


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

    def save_stock_info(self, ):
        pass


class ICrawlerRepo(metaclass=ABCMeta):
    """
    股票数据获取的接口
    """
    @abstractmethod
    def get_stock_list(self):
        pass


class CrawlerUsecase:
    def __init__(self, stock_repo: IStockRepo, crawler_repo: ICrawlerRepo):
        self.stock_repo = stock_repo
        self.crawler_repo = crawler_repo

    def get_stock_list(self):
        return self.crawler_repo.get_stock_list()
