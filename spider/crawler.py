import os
import dotenv

dotenv.load_dotenv(".env")

import tushare_api
from db_tools.mysql_db import MySQLDB

TABLE_STOCK_BASIC = os.getenv('TABLE_STOCK_BASIC')
TABLE_STOCK_DAILY = os.getenv('TABLE_STOCK_DAILY')
SQL_QUERY_TS_CODE = "SELECT ts_code from {table} wHERE name='{name}';"
SQL_QUERY_DAILY_EXISTS = "SELECT max(trade_date) as trade_date FROM {table} WHERE ts_code='{ts_code}';"


class Crawler:
    def __init__(self, mysql_obj, stock_api):
        self.mysql_obj = mysql_obj
        self.stock_api = stock_api

    def crawler_stock_info(self):
        df_info = self.stock_api.get_stock_basic()
        df_info['id'] = df_info.index + 1
        self.mysql_obj.insert(df_info, 'stock_basic')
        self.mysql_obj.alter_table(TABLE_STOCK_BASIC)

    def crawler_stock_data(self, name=None, ts_code=None, start_date=None, end_date=None):
        if not ts_code and name:
            sql_code = SQL_QUERY_TS_CODE.format(table=TABLE_STOCK_BASIC,
                                                name=name)
            df_code = self.mysql_obj.query(sql_code)
            ts_code = df_code['ts_code'].values[0]
        sql_exists = SQL_QUERY_DAILY_EXISTS.format(table=TABLE_STOCK_DAILY, ts_code=ts_code)
        df_exists = self.mysql_obj.query(sql_exists)
        if not df_exists.empty:
            start_date = df_exists['trade_date'].values[0]
        df_daily = self.stock_api.get_pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date)
        df_daily['id'] = df_daily.index + 1
        df_daily = df_daily[df_daily['trade_date'] != start_date]
        if not df_daily.empty:
            print("insert %s from %s to today" % (name, start_date))
            self.mysql_obj.insert(df_daily)

    def init(self):
        # 创建 stock_basic 表
        self.crawler_stock_info()
        # 创建 stock_daily 表
        df_daily = self.stock_api.get_pro_bar('600745.SH')
        df_daily['id'] = df_daily.index + 1
        self.mysql_obj.insert(df_daily, TABLE_STOCK_DAILY)
        self.mysql_obj.alter_table(TABLE_STOCK_DAILY)


def main():
    mysql_obj = MySQLDB()
    stock_api = tushare_api.StockApi()
    crawler_obj = Crawler(mysql_obj, stock_api)
    crawler_obj.crawler_stock_data(name='闻泰科技')
    # crawler_obj.init()


if __name__ == "__main__":
    main()
