from pykit.transport import grpc
from crawler.internal.config import config_pb2
from api.crawler.v1 import stock_info_pb2
from api.crawler.v1 import stock_info_pb2_grpc
from pykit.middleware import recovery


def NewGrpcServer(c: config_pb2.Server,
                  stock_info: stock_info_pb2_grpc.StockServiceServicer) -> grpc.Server:
    """启动 grpc server

    Args:
        c (config_pb2.Server): _description_
        stock_info (stock_v1.IStockInfoServiceHTTPServer): _description_

    Returns:
        grpc.Server: _description_
    """
    # print(c.grpc, stock_info)
    middleware = [
        recovery.Recovery()
    ]
    server = grpc.Server(address=c.grpc.addr, network=c.grpc.network,
                         middleware=middleware)
    server.register(descriptor=stock_info_pb2.DESCRIPTOR.services_by_name['StockService'],
                    register_func=stock_info_pb2_grpc.add_StockServiceServicer_to_server,
                    servicer=stock_info)
    return server
