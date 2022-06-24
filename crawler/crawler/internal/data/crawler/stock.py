'''
Description:
'''


from pandas import DataFrame
from crawler.internal.biz.crawler import IStockRepo
from crawler.internal.data.data import DB
from crawler.internal.data.sqlalchemy.schema.stock_info import StockInfo


class StockRepo(IStockRepo):
    def __init__(self, db: DB):
        self.db = db

    def get_stock_info(self, id: int):
        return StockInfo.query.filter(StockInfo.id == id).first()

    def upinsert_stock_list(self, df_stock_basic: DataFrame):
        """_summary_

        Args:
            df_stock_basic (DataFrame): _description_
        """
        df_stock_basic.to_sql(name=StockInfo.__tablename__, con=self.db.sqlalchemy_client, 
                              if_exists='replace')
