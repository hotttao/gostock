
from pykit.transport.http.context import Context
from api.crawler.v1.error_reason_pb2_erros import error_stock_not_found
from api.crawler.v1.stock_info_pb2 import StockBasicRequest, StockBasic
from api.crawler.v1.stock_info_pb2_grpc import StockServiceServicer
from crawler.internal.biz.stock_info import StockInfoUsecase


class StockInfoService(StockServiceServicer):
    def __init__(self, uc: StockInfoUsecase):
        self.uc = uc

    def GetStockInfo(self, req: StockBasicRequest, context: Context) -> StockBasic:

        res = StockBasic(ts_code='1', name='test')
        # raise error_stock_not_found(f"stock: {req.is_hs} not found")
        return res
