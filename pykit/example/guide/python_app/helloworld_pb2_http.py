
import traceback
from abc import ABCMeta
from abc import abstractmethod
from flask import request
from pykit.transport import http
from pykit.context import Context
import helloworld_pb2 as helloworld_pb2


class IGreeterServiceHTTPServer(metaclass=ABCMeta):

    @abstractmethod
    def SayMulti(context: http.Context, req: helloworld_pb2.MultiRequest) -> helloworld_pb2.HelloReply:
        pass

    @abstractmethod
    def Echo(context: http.Context, req: helloworld_pb2.MultiRequest) -> helloworld_pb2.HelloReply:
        pass

    @abstractmethod
    def SayHello(context: http.Context, req: helloworld_pb2.HelloRequest) -> helloworld_pb2.HelloReply:
        pass


def RegisterGreeterServiceHTTPServer(s: http.Server, srv: IGreeterServiceHTTPServer):
    r = s.router("/")

    r.post("/say_hello", _GreeterService_SayHello0_HTTP_Handler(r, srv))

    r.get("/helloworld/<name>", _GreeterService_SayHello1_HTTP_Handler(r, srv))

    r.post("/say_multi", _GreeterService_SayMulti0_HTTP_Handler(r, srv))

    r.get("/app/<inner_inner_name>",
          _GreeterService_SayMulti1_HTTP_Handler(r, srv))

    r.post("/echo", _GreeterService_Echo0_HTTP_Handler(r, srv))

    r.get("/echo/echo/<path:inner_inner_name>",
          _GreeterService_Echo1_HTTP_Handler(r, srv))

    pass


def _GreeterService_SayHello0_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _sayhello0_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {}
            req = helloworld_pb2.HelloRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.SayHello)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _sayhello0_hanlder


def _GreeterService_SayHello1_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _sayhello1_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {}
            req = helloworld_pb2.HelloRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.SayHello)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _sayhello1_hanlder


def _GreeterService_SayMulti0_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _saymulti0_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {}
            req = helloworld_pb2.MultiRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.SayMulti)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _saymulti0_hanlder


def _GreeterService_SayMulti1_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _saymulti1_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {'inner_inner_name': {
                'proto_key': 'inner.innerName', 'prefix': ''}}
            req = helloworld_pb2.MultiRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.SayMulti)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _saymulti1_hanlder


def _GreeterService_Echo0_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _echo0_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {}
            req = helloworld_pb2.MultiRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.Echo)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _echo0_hanlder


def _GreeterService_Echo1_HTTP_Handler(router: http.Router, srv: IGreeterServiceHTTPServer):
    def _echo1_hanlder(**kwargs):
        try:
            ctx = http.Context(
                request=request, url_params=kwargs, router=router)
            url_to_proto = {'inner_inner_name': {
                'proto_key': 'inner.innerName', 'prefix': 'echo'}}
            req = helloworld_pb2.MultiRequest()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.Echo)
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _echo1_hanlder


class IGreeterServiceHTTPClient(metaclass=ABCMeta):

    @abstractmethod
    def SayMulti(self, ctx: http.Context, req: helloworld_pb2.MultiRequest, *args,
                 **kwargs) -> helloworld_pb2.HelloReply:
        pass

    @abstractmethod
    def Echo(self, ctx: http.Context, req: helloworld_pb2.MultiRequest, *args,
             **kwargs) -> helloworld_pb2.HelloReply:
        pass

    @abstractmethod
    def SayHello(self, ctx: http.Context, req: helloworld_pb2.HelloRequest, *args,
                 **kwargs) -> helloworld_pb2.HelloReply:
        pass


class GreeterServiceHTTPClientImpl(IGreeterServiceHTTPClient):
    def __init__(self, cc: http.Client):
        self.cc = cc

    def SayMulti(self, ctx: Context, req: helloworld_pb2.MultiRequest,
                 *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/app/<inner_inner_name>"
        url_to_proto = {'inner_inner_name': {
            'proto_key': 'inner.innerName', 'prefix': ''}}
        path = http.encode_url(pattern, req, url_to_proto)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="get",
                             path=path, req_pb2=req, *args, **kwargs)
        return out, None

    def Echo(self, ctx: Context, req: helloworld_pb2.MultiRequest,
             *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/echo/echo/<path:inner_inner_name>"
        url_to_proto = {'inner_inner_name': {
            'proto_key': 'inner.innerName', 'prefix': 'echo'}}
        path = http.encode_url(pattern, req, url_to_proto)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="get",
                             path=path, req_pb2=req, *args, **kwargs)
        return out, None

    def SayHello(self, ctx: Context, req: helloworld_pb2.HelloRequest,
                 *args, **kwargs) -> helloworld_pb2.HelloReply:
        pattern = "/helloworld/<name>"
        url_to_proto = {}
        path = http.encode_url(pattern, req, url_to_proto)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="get",
                             path=path, req_pb2=req, *args, **kwargs)
        return out, None


def NewGreeterServiceHTTPClient(client: http.Client) -> IGreeterServiceHTTPClient:
    return GreeterServiceHTTPClientImpl(client)
