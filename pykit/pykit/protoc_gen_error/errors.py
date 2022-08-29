import re
import os
import sys
from typing import List, Dict
from collections import defaultdict
from google.protobuf.compiler import plugin_pb2
from google.protobuf import descriptor_pb2
# from google.protobuf import type_pb2
from google.api import annotations_pb2
from google.api import http_pb2
from google.protobuf.descriptor import FieldDescriptor
import logging

logger = logging.getLogger('proto-python-error')


def generate_error_files(request: plugin_pb2.CodeGeneratorRequest,
                         omitempty: bool = True) -> plugin_pb2.CodeGeneratorResponse:
    """生成错误处理的代码

    Args:
        request (plugin_pb2.CodeGeneratorRequest): _description_
        omitempty (bool, optional): _description_. Defaults to True.

    Returns:
        plugin_pb2.CodeGeneratorResponse: _description_
    """
    logger.info("start error out")
    response = plugin_pb2.CodeGeneratorResponse()
    for proto_file in request.proto_file:
        f = response.file.add()
        f.name = f'{os.path.splitext(proto_file.name)[0]}_pb2_error.py'
        f.content = "import json"
    return response
