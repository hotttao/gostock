
from crawler.internal.config.config_pb2 import Server
from pykit.transport import http


def NewHTTPServer(c: Server) -> http.Server:

    srv = http.NewServer()
    # srv.Handle("/metrics", promhttp.Handler())
    # v1.RegisterGreeterHTTPServer(srv, greeter)
    # evaluate_v2.RegisterIncomeHTTPServer(srv, income)
    # stock_v1.RegisterStockInfoServiceHTTPServer(srv, stock)
    return srv
