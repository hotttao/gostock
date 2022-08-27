from werkzeug.datastructures import ImmutableMultiDict
from pykit.transport.http.binding import multi_dict_to_message
from pykit.protoc_gen_http.utils import get_attrs
from helloworld_pb2 import HelloRequest, Inner, MultiRequest, Inner
from google.protobuf.descriptor import FieldDescriptor


def main():
    pass


if __name__ == '__main__':
    d = ImmutableMultiDict([('name', 'tao'), ('inner', "{'inner_id': 2}"), (
        'nums', '1'), ('nums', '2'), ('metadata', "{'about': 'abc'}"), ('is_true', 'True')])
    pb = MultiRequest()
    # print(get_attrs(pb))
    # print(pb.ListFields())
    # print(get_attrs(pb.DESCRIPTOR))
    # print(get_attrs(pb.DESCRIPTOR.fields_by_name['inner']))
    pb_inner = pb.DESCRIPTOR.fields_by_name['inner']

    multi_dict_to_message(d, pb)
