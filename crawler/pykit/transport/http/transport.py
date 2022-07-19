from flask import Request
from werkzeug.datastructures import Headers
from pykit import transport
from pykit.context import Context


class Transport(transport.ITransporter):
    def __init__(self, endpoint: str, operation: str, request_header: Headers, 
                 reply_header: Headers, kind: str = 'http',
                 request: Request = None, path_template: str = ''):
        self.endpoint = endpoint
        self.operation = operation
        self.request_header = request_header
        self.reply_header = reply_header
        self.kind = kind
        self.request = request
        self.path_template = path_template


def set_operation(ctx: Context, op: str):
    #  SetOperation sets the transport operation.
    tr = transport.from_server_context(ctx)
    if tr:
        tr.operation = op
