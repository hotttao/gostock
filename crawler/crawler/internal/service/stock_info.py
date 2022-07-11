
from typing import Tuple
from pykit.transport.http.context import Context
from api.crawler.v1.stock_info_pb2 import StockBasicRequest, StockBasic
from api.crawler.v1.stock_info_pb2_grpc import StockServiceServicer
from crawler.internal.biz.stock_info import StockInfoUsecase


class StockInfoService(StockServiceServicer):
    def __init__(self, uc: StockInfoUsecase):
        self.uc = uc

    def GetStockInfo(self, req: StockBasicRequest, context: Context) -> Tuple[StockBasic]:
        # request = context.request
        # print(request.headers, request.accept_charsets, request.accept_mimetypes)
        # print(request.content_type, request.content_encoding)
        res = StockBasic(ts_code='1', name='test')
        return res
