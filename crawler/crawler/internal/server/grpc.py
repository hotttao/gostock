from pykit.transport import grpc
from crawler.internal.config import config_pb2
from api.stock.v1 import stock_pb2_grpc


def NewGrpcServer(c: config_pb2.Server, stock_info: stock_pb2_grpc.StockServiceServicer) -> grpc.Server:
    """启动 grpc server

    Args:
        c (config_pb2.Server): _description_
        stock_info (stock_v1.IStockInfoServiceHTTPServer): _description_

    Returns:
        grpc.Server: _description_
    """
    print(c.grpc, stock_info)
    server = grpc.Server(address=c.grpc.addr, network=c.grpc.network)
    server.register(stock_pb2_grpc.add_StockServiceServicer_to_server, stock_info)
    return server
