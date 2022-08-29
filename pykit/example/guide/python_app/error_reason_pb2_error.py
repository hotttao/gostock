
from pykit import errors
import error_reason_pb2 as error_reason_pb2

# This is a compile-time assertion to ensure that this generated file
# is compatible with the kratos package it is being compiled against.


def is_stock_not_found(err: Exception) -> bool:
    if not err:
        return False
    e = errors.from_error(err)
    reason = error_reason_pb2.ErrorReason.Name(
        error_reason_pb2.ErrorReason.STOCK_NOT_FOUND)
    return e.reason == reason and e.code == 404


def error_stock_not_found(msg: str) -> errors.Error:
    reason = error_reason_pb2.ErrorReason.Name(
        error_reason_pb2.ErrorReason.STOCK_NOT_FOUND)
    return errors.Error(code=404, reason=reason, message=msg)


def is_node_not_found(err: Exception) -> bool:
    if not err:
        return False
    e = errors.from_error(err)
    reason = error_reason_pb2.ErrorReason.Name(
        error_reason_pb2.ErrorReason.NODE_NOT_FOUND)
    return e.reason == reason and e.code == 500


def error_node_not_found(msg: str) -> errors.Error:
    reason = error_reason_pb2.ErrorReason.Name(
        error_reason_pb2.ErrorReason.NODE_NOT_FOUND)
    return errors.Error(code=500, reason=reason, message=msg)
