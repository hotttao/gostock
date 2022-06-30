from crawler.internal.config.config_pb2 import Bootstrap

from crawler.internal.data.crawler.tushare_api import TuShareApi
from crawler.internal.data.stock_info import StockRepo
from crawler.internal.data.data import DB, NewRedisClient, NewSqlalchemyClient

from crawler.internal.biz.stock_info import StockInfoUsecase
from crawler.internal.service.stock_info import StockInfoService


def wire_stock_info(config: Bootstrap):
    sqlalchemy_client = NewSqlalchemyClient(config)
    redis_client = NewRedisClient(config)
    db = DB(sqlalchemy_client=sqlalchemy_client,
            redis_client=redis_client)

    crawler_repo = TuShareApi(config)
    stock_info_repo = StockRepo(db=db)
    stock_info_usecase = StockInfoUsecase(crawler_repo=crawler_repo, stock_repo=stock_info_repo)
    stock_info_service = StockInfoService(uc=stock_info_usecase)
    return stock_info_usecase, stock_info_service
