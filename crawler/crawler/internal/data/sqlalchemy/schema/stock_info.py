from crawler.internal.data.sqlalchemy.client import Base
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)


class StockInfo(Base):
    __tablename__ = 'stock_infos'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(), nullable=False)  # Y	TS代码
    symbol = Column(String(), nullable=False)  # Y	股票代码
    name = Column(String(), nullable=False)  # Y	股票名称
    area = Column(String(), nullable=False)  # Y	地域
    industry = Column(String(), nullable=False)  # Y	所属行业
    fullname = Column(String(), nullable=False)  # N	股票全称
    enname = Column(String(), nullable=False)  # N	英文全称
    cnspell = Column(String(), nullable=False)  # N	拼音缩写
    market = Column(String(), nullable=False)  # Y	市场类型（主板/创业板/科创板/CDR）
    exchange = Column(String(), nullable=True)  # N	交易所代码
    curr_type = Column(String(), nullable=True)  # N	交易货币
    list_status = Column(String(), nullable=True)  # N	上市状态 L上市 D退市 P暂停上市
    list_date = Column(DateTime(), nullable=False)  # Y	上市日期
    delist_date = Column(DateTime(), nullable=True)  # N	退市日期
    is_hs = Column(String(), nullable=True)  # N	是否沪深港通标的，N否 H沪股通 S深股通
