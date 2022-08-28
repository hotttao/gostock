import pandas as pd
from werkzeug.datastructures import ImmutableMultiDict
from pykit.transport.http.binding import multi_dict_to_message
from pykit.protoc_gen_http.utils import get_attrs
from helloworld_pb2 import MultiRequest, DESCRIPTOR

from google.api_core.path_template import transcode
from google.api import http_pb2
from google.api import annotations_pb2


pd.set_option('display.max_colwidth', None)


def main():
    pass


def parse_pb2():
    d = ImmutableMultiDict([('inner.innerId', '1'), ('inner.innerName', 'inner_tsong'),
                            ('isTrue', 'true'),
                            ('metadata[detail]', 'sky'),
                            ('metadata[path]', '/about'),
                            ('name', 'tsong'),
                            ('nums', '1'), ('nums', '2')])
    pb = MultiRequest()
    # req = MultiRequest(name='tao', inner=Inner(inner_name='tsong', inner_id=2), nums=[1, 2],
    #                    metadata={"about": "abc"}, is_true=True)
    print(get_attrs(pb))
    # print(pb.ListFields())
    # print(get_attrs(pb.DESCRIPTOR))
    # print(pb.DESCRIPTOR.fields_by_camelcase_name)
    # print(pb.DESCRIPTOR.fields_by_name)
    # print(get_attrs(pb.DESCRIPTOR.fields_by_name['metadata']))
    # pb_inner = getattr(req, 'inner')
    # print(get_attrs(pb_inner))
    # print(get_attrs(pb.DESCRIPTOR.fields_by_name['metadata'].message_type))

    message_dict = multi_dict_to_message(d, pb)
    print(message_dict)
    # print(MessageToString(req))


def parse_http_rule(rule: http_pb2.HttpRule):
    req = {}
    pattern = rule.WhichOneof('pattern')
    pattern_map = {
        'get': (rule.get, 'get'),
        'put': (rule.put, "put"),
        'post': (rule.post, "post"),
        'delete': (rule.delete, "delete"),
        'patch': (rule.patch, "patch"),
        'custom': (rule.custom.path, rule.custom.kind),
    }
    if pattern in pattern_map:
        path, method = pattern_map[pattern]
        body = rule.body
        req['uri'] = path
        req['body'] = body
        req['method'] = method
    return req


def http_rule():
    greeter = DESCRIPTOR.services_by_name['Greeter']
    # print(get_attrs(greeter))

    for method in greeter.methods[1:2]:
        http_options = []
        http_rule = method.GetOptions().Extensions[annotations_pb2.http]
        http_options.append(parse_http_rule(http_rule))
        # for bind in http_rule.additional_bindings:
        # http_options.append(parse_http_rule(bind))
        print(http_options)
        print(transcode(http_options))


if __name__ == '__main__':
    # http_rule()
    parse_pb2()
