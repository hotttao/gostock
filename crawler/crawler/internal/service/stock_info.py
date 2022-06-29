from typing import Tuple
from pykit.context import Context
from api.stock.v1.stock_pb2 import StockBasicRequest, StockBasic
from api.stock.v1.stock_pb2_http import IStockInfoServiceHTTPServer
from crawler.internal.biz.stock_info import StockInfoUsecase


class StockInfoService(IStockInfoServiceHTTPServer):
    def __init__(self, uc: StockInfoUsecase):
        self.uc = uc

    def GetStockInfo(context: Context, req: StockBasicRequest) -> Tuple[StockBasic, Exception]:
        pass