import sys
import argparse
from google.protobuf.compiler import plugin_pb2
from pykit.protoc_gen_error.errors import generate_error_files
from pykit.protoc_gen_error import __version__


parser = argparse.ArgumentParser()

parser.add_argument('--version', '-v', action='store_true',
                    default=False, dest='version',
                    help='show the version')

parser.add_argument('--omitempty', '-o', action='store_true',
                    dest='omitempty',
                    help='omit if google.api is empty',
                    default=True)

args = parser.parse_args()


def gen_error():
    """ Calls the autogenerator """
    if args.version:
        print(f'protoc-gen-python-http version: {__version__}')
        return
    # Parse request
    request = plugin_pb2.CodeGeneratorRequest()
    request.ParseFromString(sys.stdin.buffer.read())

    # Generate code and output it to stdout
    response = generate_error_files(request, args.omitempty)
    sys.stdout.buffer.write(response.SerializeToString())
