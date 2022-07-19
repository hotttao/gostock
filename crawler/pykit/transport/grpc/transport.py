from typing import Callable, List
from werkzeug.datastructures import Headers
from pykit import transport


class Transport(transport.ITransporter):
    def __init__(self, endpoint: str, operation: str, request_header: Headers,
                 reply_header: Headers, kind: str = 'grpc',
                 filters: List[Callable] = None):
        self.endpoint = endpoint
        self.operation = operation
        self.request_header = request_header
        self.reply_header = reply_header
        self.kind = kind
        self.filters = filters
