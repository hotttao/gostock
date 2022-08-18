"""

"""

import grpc
from api.crawler.v1.stock_info_pb2 import StockBasicRequest
from api.crawler.v1.stock_info_pb2_grpc import StockServiceStub
from api.crawler.v1.stock_info_pb2_http import NewStockInfoServiceHTTPClient
from pykit.transport.http.client import Client
from pykit.context import Context
from pykit.contrib.registry.consul import ConsulImp, ConsulClient
from google.protobuf.json_format import MessageToJson


# def test_get_stock_info_grpc():
#     with grpc.insecure_channel('localhost:9001') as channel:
#         channel.unary_unary
#         stub = StockServiceStub(channel)
#         response = stub.GetStockInfo(StockBasicRequest(is_hs='H'))
#     print("Greeter client received: " + MessageToJson(response, indent=4))


def test_get_stock_info_http():
    client = ConsulClient(host="127.0.0.1", port=8500)
    discovery = ConsulImp(client=client)
    client = Client(
        endpoint="discovery://default/crawler",
        discovery=discovery
    )

    stock_client = NewStockInfoServiceHTTPClient(client=client)
    req = StockBasicRequest(id=1)
    ctx = Context()
    stock_client.GetStockInfo(ctx=ctx, req=req)
    client.close()
