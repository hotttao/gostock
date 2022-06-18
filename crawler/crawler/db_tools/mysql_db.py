import os
import pandas
from sqlalchemy import create_engine

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DEFAULT_DB = os.getenv("MYSQL_DEFAULT_DB")
MYSQL_DSN = os.getenv("MYSQL_DSN")

MYSQL_DSN_FORMAT = "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DEFAULT_DB}"
SQL_SCHEMA = 'ALTER TABLE {table} MODIFY id INT NOT NULL PRIMARY KEY;'

class MySQLDB:
    def __init__(self, user=MYSQL_USER, password=MYSQL_PASSWORD,
                 host=MYSQL_HOST, port=MYSQL_PORT,
                 default_db=MYSQL_DEFAULT_DB, dsn=MYSQL_DSN):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dsn = dsn or \
                   MYSQL_DSN_FORMAT.format(USER=user, PASSWORD=password,
                                           HOST=host, PORT=port,
                                           DEFAULT_DB=default_db)
        print(dsn)
        self.engine = create_engine(self.dsn)

    def query(self, sql):
        df = pandas.read_sql(sql, self.engine)
        return df

    def insert(self, df, table):
        df.to_sql(table, self.engine, if_exists="append",index=False)

    def alter_table(self, table):
        with self.engine.connect() as conn:
            sql_schema = SQL_SCHEMA.format(table=table)
            conn.execute(sql_schema)

