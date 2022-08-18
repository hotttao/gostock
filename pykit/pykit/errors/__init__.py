
import copy
import grpc
from typing import Dict
from pykit.errors.errors_pb2 import Status
from pykit.transport.http import status as http_status
from google.protobuf.json_format import MessageToDict, ParseDict


# UnknownCode is unknown code for error info.
UnknownCode = 500
# UnknownReason is unknown reason for error info.
UnknownReason = ""
# SupportPackageIsVersion1 this constant should not be referenced by any other code.
SupportPackageIsVersion1 = True


# Error is a status error.
class Error(Exception):
    def __init__(self, code: int, reason: str, message: str, metadata: Dict = None, cause=None):
        metadata = metadata or {}
        self.code = code
        self.reason = reason
        self.message = message
        self.metadata = metadata
        self.cause = cause

    @classmethod
    def from_dict(cls, error_dict):
        """_summary_

        Args:
            dict (_type_): _description_
        """
        status = ParseDict(error_dict, Status())
        return cls(code=status.code, reason=status.reason,
                   message=status.message, metadata=status.metadata)

    def clone(self) -> Exception:
        metadata = copy.deepcopy(self.metadata)
        return Error(cause=self.cause, code=self.code,
                     message=self.message, metadata=metadata,
                     reason=self.reason)

    def to_status(self):
        print('&&&&&&&&&&&&&&&&&&&&')
        status = Status(code=self.code, reason=self.reason, message=self.message, metadata=self.metadata)
        a = MessageToDict(status)
        print('==============')
        print(type(a))
        return status

    def __str__(self):
        s = (f"error: code = {self.code} reason = {self.reason} "
             f"message = {self.message} metadata = {self.metadata} cause = {self.cause}")
        return s

    __repr__ = __str__

    # Unwrap provides compatibility for Go 1.13 error chains.
    def unwrap(self):
        return self.cause
    # Is matches each error in the chain with the target value.

    @classmethod
    def Is(cls, err):
        if isinstance(err, cls):
            return True
        return False

    def __eq__(self, error: Exception):
        if self.Is(error):
            return error.Code == self.Code & error.Reason == self.Reason
        return False
    # WithCause with the underlying cause of the error.

    def with_cause(self, cause: Exception):
        err = self.clone()
        err.cause = cause
        return err

    # WithMetadata with an MD formed by the mapping of key, value.
    def With_metadata(self, md: Dict):
        err = self.clone()
        err.metadata = md
        return err

    # def to_grpc_status():
        # GRPCStatus returns the Status represented by se.
        # s = grpc.Status()
        # s, _ = status.New(httpstatus.ToGRPCCode(int(e.Code)), e.Message).
        #     WithDetails(& errdetails.ErrorInfo{
        #         Reason: e.Reason,
        #         Metadata: e.Metadata,
        #     })
        # return s


def code(err: Exception) -> int:
    # Code returns the http code for an error.
    # It supports wrapped errors.
    if not err:
        return 200
    return int(from_error(err).Code)


def reason(err: Exception) -> str:
    # Reason returns the reason for a particular error.
    # It supports wrapped errors.
    if not err:
        return UnknownReason

    return from_error(err).Reason


def from_error(err: Exception) -> Error:
    # FromError try to convert an error to *Error.
    # It supports wrapped errors.
    if not err:
        return None
    if Error.Is(err):
        return err
    if not isinstance(err, grpc.RpcError):
        return Error(code=UnknownCode, reason=UnknownReason, message=str(err))

    ret = Error(
        http_status.from_grpc_code(err.code()),
        UnknownReason,
        message=err.details(),
    )
    # for _, detail := range gs.Details() {
    #     switch d := detail.(type) {
    #         case * errdetails.ErrorInfo:
    #         ret.Reason = d.Reason
    #         return ret.WithMetadata(d.Metadata)
    #     }
    # }
    return ret
