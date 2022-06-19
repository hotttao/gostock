class Connection:
    def __init__(self, sqlalchemy_client, redis_client) -> None:
        self.sqlalchemy_client = sqlalchemy_client
        self.redis_client = redis_client


def NewSqlalchemyClient(config):
    """_summary_

    Args:
        config (_type_): _description_
    """


def NewRedisClient(config):
    """_summary_

    Args:
        config (_type_): _description_
    """
