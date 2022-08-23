
                    
from abc import ABCMeta
from abc import abstractmethod
from pykit.transport import http
from pykit.context import Context
import helloworld_pb2 as helloworld_pb2


class IGreeterServiceHTTPServer(metaclass=ABCMeta):


    @abstractmethod
    def SayHello(context: http.Context, req: helloworld_pb2.HelloRequest) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayHello(context: http.Context, req: helloworld_pb2.HelloRequest) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayMulti(context: http.Context, req: helloworld_pb2.MultiRequest) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayMulti(context: http.Context, req: helloworld_pb2.MultiRequest) -> helloworld_pb2.HelloReply:
        pass



def RegisterGreeterServiceHTTPServer(s: http.Server, srv: IGreeterServiceHTTPServer):
    r = s.router("/")
    
    r.get("/stock/<id>", _GreeterService_SayHello_HTTP_Handler(r, srv))
    
    r.get("/stock/<id>", _GreeterService_SayHello_HTTP_Handler(r, srv))
    
    r.get("/stock/<id>", _GreeterService_SayMulti_HTTP_Handler(r, srv))
    
    r.get("/stock/<id>", _GreeterService_SayMulti_HTTP_Handler(r, srv))
    
    pass


def _GreeterService_SayHello_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _sayhello_hanlder(ctx: http.Context):
        req = helloworld_pb2.HelloRequest()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.SayHello)
        reply = h(req, ctx)
        return ctx.result(reply)
    return _sayhello_hanlder


def _GreeterService_SayHello_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _sayhello_hanlder(ctx: http.Context):
        req = helloworld_pb2.HelloRequest()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.SayHello)
        reply = h(req, ctx)
        return ctx.result(reply)
    return _sayhello_hanlder


def _GreeterService_SayMulti_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _saymulti_hanlder(ctx: http.Context):
        req = helloworld_pb2.MultiRequest()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.SayMulti)
        reply = h(req, ctx)
        return ctx.result(reply)
    return _saymulti_hanlder


def _GreeterService_SayMulti_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _saymulti_hanlder(ctx: http.Context):
        req = helloworld_pb2.MultiRequest()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.SayMulti)
        reply = h(req, ctx)
        return ctx.result(reply)
    return _saymulti_hanlder



class IGreeterServiceHTTPClient(metaclass=ABCMeta):

    @abstractmethod
    def SayHello(self, ctx: http.Context, req: helloworld_pb2.HelloRequest, *args,
                     **kwargs) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayHello(self, ctx: http.Context, req: helloworld_pb2.HelloRequest, *args,
                     **kwargs) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayMulti(self, ctx: http.Context, req: helloworld_pb2.MultiRequest, *args,
                     **kwargs) -> helloworld_pb2.HelloReply:
        pass


    @abstractmethod
    def SayMulti(self, ctx: http.Context, req: helloworld_pb2.MultiRequest, *args,
                     **kwargs) -> helloworld_pb2.HelloReply:
        pass



class GreeterServiceHTTPClientImpl(IGreeterServiceHTTPClient):
    def __init__(self, cc: http.Client):
        self.cc = cc


    def SayHello(self, ctx: Context, req: helloworld_pb2.HelloRequest,
                     *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/stock/<id>"
        path = http.encode_url(pattern, req)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="GET", path=path, req_pb2=req, *args, **kwargs)
        return out, None

    def SayHello(self, ctx: Context, req: helloworld_pb2.HelloRequest,
                     *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/stock/<id>"
        path = http.encode_url(pattern, req)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="GET", path=path, req_pb2=req, *args, **kwargs)
        return out, None

    def SayMulti(self, ctx: Context, req: helloworld_pb2.MultiRequest,
                     *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/stock/<id>"
        path = http.encode_url(pattern, req)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="GET", path=path, req_pb2=req, *args, **kwargs)
        return out, None

    def SayMulti(self, ctx: Context, req: helloworld_pb2.MultiRequest,
                     *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/stock/<id>"
        path = http.encode_url(pattern, req)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="GET", path=path, req_pb2=req, *args, **kwargs)
        return out, None


def NewGreeterServiceHTTPClient(client: http.Client) -> IGreeterServiceHTTPClient:
    return GreeterServiceHTTPClientImpl(client)                    
