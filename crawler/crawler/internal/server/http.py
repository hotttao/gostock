

from crawler.internal.config import config_pb2
from api.crawler.v1 import stock_info_pb2_http as stock_v1
from pykit.transport import http
from pykit.middleware.recovery import Recovery


def NewHTTPServer(c: config_pb2.Server, stock_info: stock_v1.IStockInfoServiceHTTPServer) -> http.Server:
    print(c)
    middlewares = [
        Recovery()
    ]
    srv = http.Server(c.http.addr, middlewares=middlewares)
    stock_v1.RegisterStockInfoServiceHTTPServer(srv, stock_info)
    # srv.Handle("/metrics", promhttp.Handler())
    # v1.RegisterGreeterHTTPServer(srv, greeter)
    # evaluate_v2.RegisterIncomeHTTPServer(srv, income)
    # stock_v1.RegisterStockInfoServiceHTTPServer(srv, stock)
    return srv
