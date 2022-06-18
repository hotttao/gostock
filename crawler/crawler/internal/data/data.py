

class Data:
    def __init__(self, mysql_client, redis_client) -> None:
        self.mysql_client = mysql_client
        self.redis_client = redis_client
