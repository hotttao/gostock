import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from google.protobuf.json_format import MessageToJson


def test_grpc_health_check():
    """测试健康状态检测接口
    """
    with grpc.insecure_channel('192.168.2.70:9001') as channel:
        stub = health_pb2_grpc.HealthStub(channel)
        response = stub.Check(health_pb2.HealthCheckRequest())
        print("Greeter client received: " + MessageToJson(response))
