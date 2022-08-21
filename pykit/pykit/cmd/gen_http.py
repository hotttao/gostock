import sys
from google.protobuf.compiler import plugin_pb2
from pykit.protoc_gen_http.autogen import AutoGen


def main():
    """ Calls the autogenerator """
    # Parse request
    request = plugin_pb2.CodeGeneratorRequest()
    request.ParseFromString(sys.stdin.buffer.read())

    # Generate code and output it to stdout
    auto_gen_obj = AutoGen(request)
    response = auto_gen_obj.gen()
    sys.stdout.buffer.write(response.SerializeToString())


if __name__ == '__main__':
    main()
