"""
Code generated by protoc-gen-go-http. DO NOT EDIT.
versions:
protoc-gen-python-http v1.0.1
"""
from abc import ABCMeta
from abc import abstractmethod
from typing import Tuple
from flask import request
from pykit.context import Context
from pykit.transport import http
from api.stock.v1.stock_pb2 import StockBasicRequest, StockBasic


class IStockInfoServiceHTTPServer(metaclass=ABCMeta):

    @abstractmethod
    def GetStockInfo(context: Context, req: StockBasicRequest) -> Tuple[StockBasic, Exception]:
        pass


def RegisterStockInfoServiceHTTPServer(s: http.Server, srv: IStockInfoServiceHTTPServer):
    # r := s.Route("/")
    s.get("/stock/{id}", _StockInfoService_GetStockInfo0_HTTP_Handler(srv))
    pass


def _StockInfoService_GetStockInfo0_HTTP_Handler(srv: IStockInfoServiceHTTPServer):
    def _hanlder(**kwargs):
        # var in GetStockInfoRequest
        # if err := ctx.BindQuery(& in); err != nil {
        #     return err
        # }
        # if err := ctx.BindVars(& in); err != nil {
        #     return err
        # }
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        # h := ctx.Middleware(func(ctx context.Context, req interface{})(interface{}, error) {
        #     return srv.GetStockInfo(ctx, req.(*GetStockInfoRequest))
        # })
        # out, err := h(ctx, & in)
        # if err != nil {
        #     return err
        # }
        # reply == out.(*StockInfo)
        # return ctx.Result(200, reply)
        pass
    return _hanlder


class StockInfoServiceHTTPClient(metaclass=ABCMeta):

    @abstractmethod
    def GetStockInfo(self, ctx: Context, req: StockBasicRequest, *args,
                     **kwargs) -> Tuple[StockBasic, Exception]:
        pass


class StockInfoServiceHTTPClientImpl(StockInfoServiceHTTPClient):
    def __init__(self, cc: http.Client):
        self.cc = cc

    def GetStockInfo(self, ctx: Context, req: StockBasicRequest,
                     *args, **kwargs) -> Tuple[StockBasic, Exception]:
        # out = StockInfo()
        # pattern = "/stock/{id}"
        # path = binding.EncodeURL(pattern, in , true)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        # return out, err
        pass


def NewStockInfoServiceHTTPClient(client: http.Client) -> StockInfoServiceHTTPClient:
    return StockInfoServiceHTTPClientImpl(client)