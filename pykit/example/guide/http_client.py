import grpc
from helloworld_pb2 import HelloRequest
from helloworld_pb2_grpc import GreeterStub
from helloworld_pb2_http import NewStockInfoServiceHTTPClient
from pykit.transport.http.client import Client
from pykit.context import Context
from pykit.contrib.registry.consul import ConsulImp, ConsulClient
from google.protobuf.json_format import MessageToJson


def test_get_stock_info_http():
    client = ConsulClient(host="127.0.0.1", port=8500)
    discovery = ConsulImp(client=client)
    client = Client(
        endpoint="discovery://default/crawler",
        discovery=discovery
    )

    stock_client = NewStockInfoServiceHTTPClient(client=client)
    req = HelloRequest(name='tao')
    ctx = Context()
    stock_client.GetStockInfo(ctx=ctx, req=req)
    client.close()
