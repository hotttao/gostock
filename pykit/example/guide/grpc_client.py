import add_pythonpath
from pykit.transport.grpc.client import Client
from pykit.middleware.recovery import Recovery
from google.protobuf.json_format import MessageToJson
from helloworld_pb2 import HelloRequest
from helloworld_pb2_grpc import GreeterStub


add_pythonpath.log_sys_path


def start_grpc_client():
    """测试健康状态检测接口
    """
    client = Client(endpoint='192.168.2.70:9001',
                    middleware=[Recovery()])
    channel = client.dail()

    stub = GreeterStub(channel)
    response = stub.SayHello(HelloRequest(name='tao'))
    print("Greeter client received: " + MessageToJson(response))


if __name__ == '__main__':
    start_grpc_client()