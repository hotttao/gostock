from crawler.internal.config.config_pb2 import Bootstrap

from crawler.internal.data.crawler.tushare_api import TuShareApi
from crawler.crawler.internal.data.stock_info import StockRepo
from crawler.internal.data.data import DB, NewRedisClient, NewSqlalchemyClient

from crawler.crawler.internal.biz.stock_info import StockInfoUsecase


def wire_app(config: Bootstrap):
    sqlalchemy_client = NewSqlalchemyClient(config)
    redis_client = NewRedisClient(config)
    db = DB(sqlalchemy_client=sqlalchemy_client,
            redis_client=redis_client)

    crawler_repo = TuShareApi(config)
    stock_repo = StockRepo(db=db)
    crawler_usecase = StockInfoUsecase(crawler_repo=crawler_repo, stock_repo=stock_repo)
    return crawler_usecase
