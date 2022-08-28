
import requests
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
    req = MultiRequest(name='tao', inner=Inner(inner_name='tsong', inner_id=1), nums=[1, 2],
                       metadata={"path": "/about", "detail": "sky"}, is_true=True, market='B')
    ctx = Context()
    greeter_client.SayMulti(ctx=ctx, req=req)
    client.close()


def req_server_post():
    url = 'http://192.168.2.70:8001/echo_post/echo/tsong'
    headers = {'Content-Type': 'application/json'}

    # 以字典的形式构造数据
    data = {
        "name": "tao",
        "inner": {
            "innerId": 1
        },
        "nums": [
            1,
            2
        ],
        "metadata": {
            "path": "/about",
            "detail": "sky"
        },
        "isTrue": True,
        "market": "B"
    }
    # 与 get 请求一样，r 为响应对象
    r = requests.post(url, json=data)
    # r = requests.post(url, data=data)
    # 查看响应结果
    print(r.content)


if __name__ == '__main__':
    req_server_post()
    start_http_client()
