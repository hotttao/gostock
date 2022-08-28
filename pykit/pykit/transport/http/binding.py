import copy
from werkzeug.datastructures import MultiDict
from werkzeug.routing import Rule, Map
from google.protobuf.json_format import MessageToDict
from pykit.protoc_gen_http.utils import get_attrs
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.json_format import ParseDict


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
    message_dict = MessageToDict(req_pb2, preserving_proto_field_name=False)

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
    # print(url_query_map)
    # print(url_vars_map)
    # print(get_attrs(req_proto))
    url_vars_map = decode_url_vars(url_vars_map, url_to_proto)
    url_query_map = MultiDict(copy.deepcopy(url_query_map))
    url_query_map.update(url_vars_map)
    proto_pb2 = multi_dict_to_message(url_query_map, req_proto)
    return proto_pb2


def decode_url_vars(url_vars_map, url_to_proto):
    """_summary_

    Args:
        url_vars_map (_type_): _description_
        url_to_proto (_type_): _description_
    """
    proto_value_map = {}
    # url_vars_map = copy.deepcopy(url_vars_map)
    for url_var, protoc_map in url_to_proto.items():
        proto_key = protoc_map['proto_key']
        prefix = protoc_map['prefix']
        if prefix:
            prefix = f'{prefix}/'
        value = url_vars_map.pop(url_var)
        proto_value_map[proto_key] = value
        # base = url_vars_map
        # search_list = proto_key.split(".")
        # for k in search_list[:-1]:
        #     if k not in base:
        #         base[k] = {}
        #         base = base[k]
        # base[search_list[-1]] = f'{prefix}{value}'
    return proto_value_map


def parse_multi_dict_key(key, value, collect):
    if '.' in key:
        k_list = key.split('.', 1)
        k_first, k_right = k_list
        if k_first not in collect:
            collect[k_first] = {}
        parse_multi_dict_key(k_right, value, collect[k_first])
    elif '[' in key:
        k, m = key.split('[')
        m = m.replace(']', '')
        if k not in collect:
            collect[k] = {m: value}
        else:
            collect[k][m] = value
    else:
        collect[key] = value


def multi_dict_to_message(multi_dict, protoc):
    """将 ImmutableMultiDict 转换为 protoc message 格式

    Args:
        multi_dict (_type_): _description_
    """
    # print(multi_dict)
    collect = {}
    for key in multi_dict.keys():
        value = multi_dict.getlist(key)
        # if len(value) == 1:
        # value = value[0]
        parse_multi_dict_key(key, value, collect)
    message_dict = multi_dict_type_trans(collect, protoc)
    message_pb2 = ParseDict(message_dict, protoc)
    return message_pb2


def multi_dict_type_trans(trans_dict, protoc):
    """MultiDict 转换到 protoc message

    Args:
        trans_dict (_type_): 经过转换的 MultiDict 值
        protoc (_type_): _description_
    """
    message_dict = trans_dict
    for field in protoc.DESCRIPTOR.fields_by_camelcase_name.values():
        field_name = field.camelcase_name
        # print(field_name, field.label)
        if field_name not in message_dict:
            continue
        field_value = message_dict[field_name]

        if field.type in [FieldDescriptor.TYPE_ENUM]:
            value_map = dict(zip(field.enum_type.values_by_name, field.enum_type.values_by_number))
            # print(value_map)
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field_name] = [value_map.get(i, 0) for i in field_value]
            else:
                message_dict[field_name] = value_map.get(field_value[0], 0)

        elif field.type in [FieldDescriptor.TYPE_BYTES]:
            pass
        elif field.type in [FieldDescriptor.TYPE_MESSAGE, FieldDescriptor.TYPE_GROUP]:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                # 对应 map 类型
                message_dict[field_name] = {i: j[0]
                                            for i, j in message_dict[field_name].items()}
                continue
            if field_name in message_dict:
                multi_dict_type_trans(
                    message_dict[field_name], getattr(protoc, field_name))
        elif field.type in [FieldDescriptor.TYPE_DOUBLE,
                            FieldDescriptor.TYPE_FLOAT,
                            FieldDescriptor.TYPE_FIXED64,
                            FieldDescriptor.TYPE_FIXED32,
                            FieldDescriptor.TYPE_SFIXED32,
                            FieldDescriptor.TYPE_SFIXED64, ]:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field_name] = [float(i) for i in field_value]
            else:
                message_dict[field_name] = float(field_value[0])

        elif field.type in [FieldDescriptor.TYPE_INT64,
                            FieldDescriptor.TYPE_UINT64,
                            FieldDescriptor.TYPE_INT32,
                            FieldDescriptor.TYPE_UINT32,
                            FieldDescriptor.TYPE_SINT32,
                            FieldDescriptor.TYPE_SINT64, ]:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field_name] = [int(i) for i in field_value]
            else:
                message_dict[field_name] = int(field_value[0])
        elif field.type == FieldDescriptor.TYPE_BOOL:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field_name] = [i in ['True', 'true']
                                            for i in field_value]
            else:
                message_dict[field_name] = field_value[0] in [
                    'True', 'true']
        elif field.type == FieldDescriptor.TYPE_STRING:
            if field.label == FieldDescriptor.LABEL_REPEATED:
                message_dict[field_name] = field_value
            else:
                message_dict[field_name] = field_value[0]
    # print(message_dict)
    return message_dict


def flat(x):
    for key, value in x.items():
        if isinstance(value, dict):
            for k, v in flat(value):
                k = f'{key}.{k}'
                yield (k, v)
        else:
            yield (key, value)
