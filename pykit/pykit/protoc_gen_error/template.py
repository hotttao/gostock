import os
import autopep8
import json
from jinja2 import Template
from typing import List

template = Template("""
from pykit import errors
import {{ error_wrap.pb2_import }} as {{ error_wrap.pb2_import_as }}

# This is a compile-time assertion to ensure that this generated file
# is compatible with the kratos package it is being compiled against.

{% for error_info in error_wrap.error_list %}
def is_{{ error_info.camel_value }}(err: Exception) -> bool:
    if not err:
        return False
    e = errors.from_error(err)
    reason = {{ error_wrap.pb2_import_as }}.{{ error_info.name }}.Name({{ error_wrap.pb2_import_as }}.{{ error_info.name }}.{{ error_info.value }})
    return e.reason == reason and e.code == {{ error_info.http_code }}


def error_{{ error_info.camel_value }}(msg: str) -> errors.Error:
    reason = {{ error_wrap.pb2_import_as }}.{{ error_info.name }}.Name({{ error_wrap.pb2_import_as }}.{{ error_info.name }}.{{ error_info.value }})
    return errors.Error(code={{ error_info.http_code }}, reason=reason, message=msg)
{% endfor %}
""")


class ErrorInfo:
    def __init__(self, name: str, value: str, http_code: int, camel_value: str,
                 comment: str, has_comment: bool) -> None:

        self.name = name
        self.value = value
        self.http_code = http_code
        self.camel_value = camel_value
        self.comment = comment
        self.has_comment = has_comment

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'htt_code': self.http_code,
            'camel_value': self.camel_value,
            'comment': self.comment,
            'has_comment': self.has_comment,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


class ErrorWrap:
    def __init__(self, metadata: str, error_list: List[ErrorInfo] = None):
        self.error_list = error_list or []
        self.metadata = metadata

    def append(self, error_info: ErrorInfo):
        """_summary_

        Args:
            error_info (ErrorInfo): _description_
        """
        self.error_list.append(error_info)

    def __len__(self):
        return len(self.error_list)

    @property
    def pb2_import(self):
        """protoc 对应的 python 导入路径
        """
        return f'{os.path.splitext(self.metadata)[0]}_pb2'

    @property
    def pb2_import_as(self):
        """protoc 对应的 python 导入路径
        """
        return os.path.basename(self.pb2_import)

    def execute(self) -> str:
        """_summary_

        Args:
            error_list (List[ErrorInfo]): _description_

        Returns:
            str: _description_
        """
        code = template.render(error_wrap=self)
        return autopep8.fix_code(code)
