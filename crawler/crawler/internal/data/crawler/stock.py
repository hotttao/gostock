'''
Description:
'''


from crawler.internal.biz.crawler import IStockRepo
from crawler.internal.data.data import Connection


class StockRepo(IStockRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def get_stock_info(self, id: int):
        pass

    def save_stock_info(self, ):
        pass
