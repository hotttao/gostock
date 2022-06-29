

from pykit.transport import http
from crawler.internal.config.config_pb2 import Server
from api.stock.v1 import stock_pb2_http as stock_v1


def NewHTTPServer(c: Server) -> http.Server:

    srv = http.Server()
    stock_v1.RegisterStockInfoServiceHTTPServer(srv)
    # srv.Handle("/metrics", promhttp.Handler())
    # v1.RegisterGreeterHTTPServer(srv, greeter)
    # evaluate_v2.RegisterIncomeHTTPServer(srv, income)
    # stock_v1.RegisterStockInfoServiceHTTPServer(srv, stock)
    return srv
