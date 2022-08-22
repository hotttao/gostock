import sys
import argparse
from google.protobuf.compiler import plugin_pb2
from pykit.protoc_gen_http.autogen import AutoGen
from pykit.protoc_gen_http import __version__


parser = argparse.ArgumentParser()

parser.add_argument('--version', '-v', action='store_true',
                    default=False, dest='version',
                    help='show the version')

parser.add_argument('--omitempty', '-o', action='store_true',
                    dest='omitempty',
                    help='omit if google.api is empty',
                    default=True)

args = parser.parse_args()


def gen_http():
    """ Calls the autogenerator """
    if args.version:
        print(f'protoc-gen-python-http version: {__version__}')
        return
    # Parse request
    request = plugin_pb2.CodeGeneratorRequest()
    request.ParseFromString(sys.stdin.buffer.read())

    # Generate code and output it to stdout
    auto_gen_obj = AutoGen(request)
    response = auto_gen_obj.gen(args.omitempty)
    sys.stdout.buffer.write(response.SerializeToString())
