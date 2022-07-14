
from typing import Dict, Any
from flask import Request
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict


class Context:
    def __init__(self, request: Request, url_params: Dict = None) -> None:
        self.request = request
        self.url_params = url_params or {}

    def bind(self, params: Dict[str, Any], req_proto: Any):
        """_summary_

        Args:
            params (_type_): _description_
            proto (_type_): _description_
        """
        return ParseDict(params, req_proto, ignore_unknown_fields=True)
    
    @property
    def headers(self):
        return self.request.headers

    def bind_vars(self, req_proto):
        """_summary_

        Args:
            proto (_type_): _description_
        """
        if self.url_params:
            self.bind(self.url_params, req_proto)
        params = self.request.args
        return self.bind(params, req_proto)

    def result(self, res_proto, code=200):
        """_summary_

        Args:
            code (_type_): _description_
            res_proto (_type_): _description_
        """
        return MessageToDict(res_proto), code
