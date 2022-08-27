
from helloworld_pb2 import HelloRequest, Inner, MultiRequest, Inner
from helloworld_pb2_http import GreeterServiceHTTPClientImpl
from pykit.transport.http.client import Client
from pykit.context import Context
from pykit.contrib.registry.consul import ConsulImp, ConsulClient
from google.protobuf.json_format import MessageToJson, ParseDict


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
    req = MultiRequest(name='tao', inner=Inner(inner_name='tsong', inner_id=2), nums=[1, 2],
                       metadata={"about": "abc"}, is_true=True)
    ctx = Context()
    greeter_client.SayMulti(ctx=ctx, req=req)
    client.close()


if __name__ == '__main__':
    print(ParseDict({'inner_name': "tao"}, Inner()))
    print(ParseDict({'innerName': "tao"}, Inner()))
    start_http_client()
