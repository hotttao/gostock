from sqlalchemy import create_engine
from crawler.internal.data.sqlalchemy.client import bind_engine
from crawler.internal.config.config_pb2 import Bootstrap


class DB:
    def __init__(self, sqlalchemy_client, redis_client) -> None:
        self.sqlalchemy_client = sqlalchemy_client
        self.redis_client = redis_client


def NewSqlalchemyClient(config: Bootstrap):
    """_summary_

    Args:
        config (_type_): _description_
    """
    engine = create_engine(
        config.connection.database.source,  # SQLAlchemy 数据库连接串，格式见下面
        # echo=bool(config.SQLALCHEMY_ECHO),  # 是不是要把所执行的SQL打印出来，一般用于调试
        # pool_size=int(config.SQLALCHEMY_POOL_SIZE),  # 连接池大小
        # max_overflow=int(config.SQLALCHEMY_POOL_MAX_SIZE),  # 连接池最大的大小
        # pool_recycle=int(config.SQLALCHEMY_POOL_RECYCLE),  # 多久时间主动回收连接，见下注释
    )
    bind_engine(engine=engine)
    return engine


def NewRedisClient(config):
    """_summary_

    Args:
        config (_type_): _description_
    """
