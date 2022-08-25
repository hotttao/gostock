import grpc
from helloworld_pb2 import HelloRequest
from helloworld_pb2_http import GreeterServiceHTTPClientImpl
from pykit.transport.http.client import Client
from pykit.context import Context
from pykit.contrib.registry.consul import ConsulImp, ConsulClient
from google.protobuf.json_format import MessageToJson


def start_http_client_discovery():
    client = ConsulClient(host="127.0.0.1", port=8500)
    discovery = ConsulImp(client=client)
    client = Client(
        endpoint="discovery://default/crawler",
        discovery=discovery
    )

    greeter_client = GreeterServiceHTTPClientImpl(cc=client)
    req = HelloRequest(name='tao')
    ctx = Context()
    greeter_client.GetStockInfo(ctx=ctx, req=req)
    client.close()


def start_http_client():
    client = Client(
        endpoint='http://192.168.2.70:8001',
    )

    greeter_client = GreeterServiceHTTPClientImpl(cc=client)
    req = HelloRequest(name='tao')
    ctx = Context()
    greeter_client.SayMulti(ctx=ctx, req=req)
    client.close()


if __name__ == '__main__':
    start_http_client()
