from typing import Dict, Any
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict


class Context:
    def __init__(self, reqest) -> None:
        self.request = reqest

    def bind(self, params: Dict[str, Any], req_proto: Any):
        """_summary_

        Args:
            params (_type_): _description_
            proto (_type_): _description_
        """
        return ParseDict(params, req_proto, ignore_unknown_fields=True)

    def bind_vars(self, req_proto):
        """_summary_

        Args:
            proto (_type_): _description_
        """
        params = self.request.args
        return self.bind(params, req_proto)

    def result(self, res_proto, code=200):
        """_summary_

        Args:
            code (_type_): _description_
            res_proto (_type_): _description_
        """
        return MessageToDict(res_proto), code
