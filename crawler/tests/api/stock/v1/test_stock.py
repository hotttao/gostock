"""

"""
import grpc
from api.crawler.v1.stock_info_pb2 import StockBasicRequest
from api.crawler.v1.stock_info_pb2_grpc import StockServiceStub
from google.protobuf.json_format import MessageToJson


def test_get_stock_info():
    with grpc.insecure_channel('localhost:9001') as channel:
        channel.unary_unary
        stub = StockServiceStub(channel)
        response = stub.GetStockInfo(StockBasicRequest(is_hs='H'))
    print("Greeter client received: " + MessageToJson(response, indent=4))
