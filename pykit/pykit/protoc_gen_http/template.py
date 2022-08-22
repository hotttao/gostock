from jinja2 import Template
from typing import List

template = Template("""
                    
from abc import ABCMeta
from abc import abstractmethod
from typing import Tuple
from pykit.transport import http
from pykit.context import Context
from api.crawler.v1.stock_info_pb2 import StockBasicRequest, StockBasic


class IStockInfoServiceHTTPServer(metaclass=ABCMeta):

    @abstractmethod
    def GetStockInfo(context: http.Context, req: StockBasicRequest) -> Tuple[StockBasic, Exception]:
        pass


def RegisterStockInfoServiceHTTPServer(s: http.Server, srv: IStockInfoServiceHTTPServer):
    r = s.router("/")
    r.get("/stock/<id>", _StockInfoService_GetStockInfo0_HTTP_Handler(r, srv))
    pass


def _StockInfoService_GetStockInfo0_HTTP_Handler(router: http.Router, srv: IStockInfoServiceHTTPServer):
    def _stock_info_hanlder(ctx: http.Context):
        req = StockBasicRequest()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.GetStockInfo)
        reply = h(req, ctx)
        return ctx.result(reply)
    return _stock_info_hanlder


class StockInfoServiceHTTPClient(metaclass=ABCMeta):

    @abstractmethod
    def GetStockInfo(self, ctx: http.Context, req: StockBasicRequest, *args,
                     **kwargs) -> Tuple[StockBasic, Exception]:
        pass


class StockInfoServiceHTTPClientImpl(StockInfoServiceHTTPClient):
    def __init__(self, cc: http.Client):
        self.cc = cc

    def GetStockInfo(self, ctx: Context, req: StockBasicRequest,
                     *args, **kwargs) -> Tuple[StockBasic, Exception]:
        pattern = "/stock/<id>"
        path = http.encode_url(pattern, req)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="GET", path=path, req_pb2=req, *args, **kwargs)
        return out, None


def NewStockInfoServiceHTTPClient(client: http.Client) -> StockInfoServiceHTTPClient:
    return StockInfoServiceHTTPClientImpl(client)                    

""")


class FileDetail:
    def __init__(self, comment: List[str] = None):
        self.comment = comment


class MethodDetail:
    def __init__(self, name: str, original_name: str, num: int, request: str, reply: str,
                 path: str, method: str, has_vars: bool, has_body: bool = False, body: str = '',
                 response_body: str = ''):
        """_summary_

            Args:
                name (str): _description_
                original_name (str): The parsed original name
                num (int): _description_
                request (str): _description_
                reply (str): _description_
                path (str): _description_
                method (str): _description_
                has_vars (bool): _description_
                has_body (bool): _description_
                body (str): _description_
                response_body (str): _description_

            Returns:
                _type_: _description_
        """
        self.name = name
        self.original_name = original_name
        self.num = num
        self.request = request
        self.reply = reply
        self.path = path
        self.method = method
        self.has_vars = has_vars
        self.has_body = has_body
        self.body = body
        self.response_body = response_body


class ServiceDetail:
    def __init__(self, service_type: str, service_name: str,
                 metadata: str, methods: MethodDetail = None):
        """_summary_

        Args:
            service_type (str): Greeter
            service_name (str): helloworld.Greeter
            metadata (str): api/helloworld/helloworld.proto
            methods (MethodDesc):
        """
        self.service_type = service_type
        self.service_name = service_name
        self.metadata = metadata
        self.methods = methods or []

    def execute(self) -> str:
        method_sets = {}
        for m in self.methods:
            method_sets[m.name] = m
        # 加载模板，生成代码
        return ''
