import copy
import json
from werkzeug.routing import Rule, Map
from werkzeug.datastructures import ImmutableMultiDict
from google.protobuf.json_format import MessageToDict
from pykit.protoc_gen_http.utils import get_attrs
from google.protobuf.descriptor import FieldDescriptor


def encode_url(path_template, req_pb2, url_to_proto):
    """_summary_

    Args:
        path_template (_type_): _description_
        req_pb2 (_type_): _description_
    """

    m = Map()
    rule = Rule(path_template)

    rule.bind(m)
    params = dict(flat(encode_url_vars(req_pb2, url_to_proto)))
    _, path = rule.build(params)
    return path


def encode_url_vars(req_pb2, proto_to_url):
    """将 protoc message 中的字段，映射成 url 中变量的字段名

    Args:
        req_pb2 (_type_): message ToDict 后的值
        proto_to_url (_type_): protoc 字段到 url var 的映射关系
    """
    message_dict = MessageToDict(req_pb2, preserving_proto_field_name=True)

    for url_var, var_container in proto_to_url.items():
        proto_key = var_container['proto_key']
        base = message_dict
        pre = None
        for k in proto_key.split('.'):
            pre = base
            base = base[k]
        pre.pop(proto_key.split('.')[-1])
        message_dict[url_var] = base
    print(message_dict)
    return message_dict


def decode_url(url_query_map, url_vars_map, url_to_proto, req_proto):
    """_summary_

    Args:
        url_quer_map (_type_): url 的查询参数
        url_vars_map (_type_): url 中的路径参数
        url_to_proto (_type_): url 路径参数到 proto message 的映射关系
    """
    print(url_query_map)
    print(url_vars_map)
    print(get_attrs(req_proto))
    url_vars_map = decode_url_vars(url_vars_map, url_to_proto)
    url_query_map = copy.deepcopy(url_query_map)
    url_query_map.update(url_vars_map)


def decode_url_vars(url_vars_map, url_to_proto):
    """_summary_

    Args:
        url_vars_map (_type_): _description_
        url_to_proto (_type_): _description_
    """
    url_vars_map = copy.deepcopy(url_vars_map)
    for url_var, protoc_map in url_to_proto.items():
        proto_key = protoc_map['proto_key']
        prefix = protoc_map['prefix']
        if prefix:
            prefix = f'{prefix}/'
        value = url_vars_map.pop(url_var)

        base = url_vars_map
        search_list = proto_key.split(".")
        for k in search_list[:-1]:
            if k not in base:
                base[k] = {}
                base = base[k]
        base[search_list[-1]] = f'{prefix}{value}'
    return url_vars_map


def multi_dict_to_message(multi_dict, protoc):
    """MultiDict 转换到 protoc message

    Args:
        multi_dict (_type_): _description_
        protoc (_type_): _description_
    """
    message_dict = {}
    for field in protoc.DESCRIPTOR.fields_by_name.values():

        if field.type in [FieldDescriptor.TYPE_ENUM]:
            pass
        elif field.type in [FieldDescriptor.TYPE_BYTES]:
            pass
        elif field.type in [FieldDescriptor.TYPE_MESSAGE, FieldDescriptor.TYPE_GROUP]:
            print(type(multi_dict.get(field.name)), multi_dict.get(field.name))
            mulit_data = ImmutableMultiDict()
            
            # mulit_data.update(multi_dict.get(field.name))
            message_dict_sub = message_dict(mulit_data, field)
            message_dict.update(message_dict_sub)
        elif field.type in [FieldDescriptor.TYPE_DOUBLE,
                            FieldDescriptor.TYPE_FLOAT,
                            FieldDescriptor.TYPE_FIXED64,
                            FieldDescriptor.TYPE_FIXED32,
                            FieldDescriptor.TYPE_SFIXED32,
                            FieldDescriptor.TYPE_SFIXED64, ]:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field.name] = [float(i) for i in multi_dict.getlist(field.name)]
            else:
                message_dict[field.name] = float(multi_dict.get(field.name))

        elif field.type in [FieldDescriptor.TYPE_INT64,
                            FieldDescriptor.TYPE_UINT64,
                            FieldDescriptor.TYPE_INT32,
                            FieldDescriptor.TYPE_UINT32,
                            FieldDescriptor.TYPE_SINT32,
                            FieldDescriptor.TYPE_SINT64, ]:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field.name] = [int(i) for i in multi_dict.getlist(field.name)]
            else:
                message_dict[field.name] = int(multi_dict.get(field.name))
        elif field.type == FieldDescriptor.TYPE_BOOL:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field.name] = [i in ['True', 'true']
                                            for i in multi_dict.getlist(field.name)]
            else:
                message_dict[field.name] = multi_dict.get(field.name) in [
                    'True', 'true']
        elif field.type == FieldDescriptor.TYPE_STRING:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field.name] = multi_dict.getlist(field.name)
            else:
                message_dict[field.name] = multi_dict.get(field.name)
    print(message_dict)
    return message_dict


def flat(x):
    for key, value in x.items():
        if isinstance(value, dict):
            for k, v in flat(value):
                k = f'{key}.{k}'
                yield (k, v)
        else:
            yield (key, value)
