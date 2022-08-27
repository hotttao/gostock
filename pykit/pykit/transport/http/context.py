
from typing import Dict, Any
from flask import Request, Response
# from pykit.transport.http import Router
from google.protobuf.json_format import ParseDict
from pykit.transport.http.binding import decode_url


class Context:
    def __init__(self, router, request: Request, url_params: Dict = None) -> None:
        self.router = router
        self.request = request
        self.response = Response()
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

    def bind_vars(self, req_proto, url_to_proto):
        """_summary_

        Args:
            req_proto (_type_): _description_
            url_to_proto (_type_): url 中的变量到  proto message 字段的映射关系
        """

        return decode_url(url_query_map=self.request.args,
                          url_vars_map=self.url_params, url_to_proto=url_to_proto,
                          req_proto=req_proto)

    def result(self, res_proto, code=200):
        """_summary_

        Args:
            code (_type_): _description_
            res_proto (_type_): _description_
        """
        self.response.status = code
        self.router.srv.encoder_response(request=self.request, response=self.response,
                                         v=res_proto)
        return self.response
