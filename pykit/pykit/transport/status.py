import http
import grpc


# ClientClosed is non-standard http status code,
# which defined by nginx.
# https:#httpstatus.in/499/
ClientClosed = 499


# ToGRPCCode converts a HTTP error code into the corresponding gRPC response status.
# See: https:#github.com/googleapis/googleapis/blob/master/google/rpc/code.proto
HttpToGRPCCode = {
    http.HTTPStatus.OK: grpc.StatusCode.OK,
    http.HTTPStatus.BAD_REQUEST: grpc.StatusCode.INVALID_ARGUMENT,
    http.HTTPStatus.UNAUTHORIZED: grpc.StatusCode.UNAUTHENTICATED,
    http.HTTPStatus.FORBIDDEN: grpc.StatusCode.PERMISSION_DENIED,
    http.HTTPStatus.NOT_FOUND: grpc.StatusCode.NOT_FOUND,
    http.HTTPStatus.CONFLICT: grpc.StatusCode.ABORTED,
    http.HTTPStatus.TOO_MANY_REQUESTS: grpc.StatusCode.RESOURCE_EXHAUSTED,
    http.HTTPStatus.INTERNAL_SERVER_ERROR: grpc.StatusCode.INTERNAL,
    http.HTTPStatus.NOT_IMPLEMENTED: grpc.StatusCode.UNIMPLEMENTED,
    http.HTTPStatus.SERVICE_UNAVAILABLE: grpc.StatusCode.UNAVAILABLE,
    http.HTTPStatus.GATEWAY_TIMEOUT: grpc.StatusCode.DEADLINE_EXCEEDED,
    ClientClosed: grpc.StatusCode.CANCELLED,
}


# FromGRPCCode converts a gRPC error code into the corresponding HTTP response status.
# See: https:#github.com/googleapis/googleapis/blob/master/google/rpc/code.proto
GRPCToHttpCode = {j: i for i, j in HttpToGRPCCode.items()}


def to_grpc_code(code: int):
    # ToGRPCCode converts an HTTP error code into the corresponding gRPC response status.
    return HttpToGRPCCode.get(code, grpc.StatusCode.UNKNOWN)


# FromGRPCCode converts a gRPC error code into the corresponding HTTP response status.
def from_grpc_code(code):
    return GRPCToHttpCode.get(code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
