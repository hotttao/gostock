from pykit.transport.grpc.client import Client
from pykit.middleware.recovery import Recovery
from google.protobuf.json_format import MessageToJson
from api.crawler.v1.stock_info_pb2 import StockBasicRequest
from api.crawler.v1.stock_info_pb2_grpc import StockServiceStub


def test_grpc_stock_info():
    """测试健康状态检测接口
    """
    client = Client(endpoint='192.168.2.70:9001',
                    middleware=[Recovery()])
    channel = client.dail()

    stub = StockServiceStub(channel)
    response = stub.GetStockInfo(StockBasicRequest(id=1))
    print("Greeter client received: " + MessageToJson(response))
