from werkzeug.routing import Rule, Map
from google.protobuf.json_format import MessageToDict


def encode_url(path_template, req_pb2):
    """_summary_

    Args:
        path_template (_type_): _description_
        req_pb2 (_type_): _description_
    """
    params = MessageToDict(req_pb2)
    m = Map()
    rule = Rule(path_template)

    rule.bind(m)
    _, path = rule.build(params)
    return path
