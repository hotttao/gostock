from typing import Dict


class Error:
    def __init__(self, code: int, reason: str, message: str, metadata: Dict[str, str] = None):
        self.code = code
        self.reason = reason
        self.message = message
        self.metadata = metadata

    def to_dict(self):
        # {
        #     # 错误码，跟 http - status 一致，并且在 grpc 中可以转换成 grpc - status
        #     "code": 500,
        #     # 错误原因，定义为业务判定错误码
        #     "reason": "USER_NOT_FOUND",
        #     # 错误信息，为用户可读的信息，可作为用户提示内容
        #     "message": "invalid argument error",
        #     # 错误元信息，为错误添加附加可扩展信息
        #     "metadata": {
        #         "foo": "bar"
        #     }
        # }
        d = {
            'code': self.code,
            'reason': self.reason,
            'message': self.message,
            'metadata': self.metadata
        }
        return d
