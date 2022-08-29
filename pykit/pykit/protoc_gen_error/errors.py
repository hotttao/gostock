import os
import sys
from typing import List
from google.protobuf.compiler import plugin_pb2
from google.protobuf import descriptor_pb2
from pykit.errors import errors_pb2
from pykit.protoc_gen_error.template import ErrorInfo
from pykit.protoc_gen_error.template import ErrorWrap
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
        enum_list = proto_file.enum_type
        if not enum_list or (omitempty and not has_error_extensions(enum_list)):
            continue
        logger.info(f"{proto_file.name} exits error extension")

        f = response.file.add()
        f.name = f'{os.path.splitext(proto_file.name)[0]}_pb2_error.py'
        contents = []
        for enum_desc in enum_list:
            error_contents = gen_errors_reason(file_desc=proto_file,
                                               file_generate=f, enum_desc=enum_desc)
            contents.append(error_contents)
        f.content = '\n'.join(contents)
    return response


def has_error_extensions(enum_list: List[descriptor_pb2.EnumDescriptorProto]):
    """判断 protobuf 是否有 error 扩展

    Args:
        enum_list (List[descriptor_pb2.EnumDescriptorProto]): _description_
    """
    for enmu_desc in enum_list:

        if errors_pb2.default_code in enmu_desc.options.Extensions:
            return True
    return False


def gen_errors_reason(file_desc: descriptor_pb2.FileDescriptorProto,
                      file_generate: plugin_pb2.CodeGeneratorResponse.File,
                      enum_desc: descriptor_pb2.EnumDescriptorProto):
    if errors_pb2.default_code not in enum_desc.options.Extensions:
        return

    default_code = enum_desc.options.Extensions[errors_pb2.default_code]
    logger.info(f'{type(default_code)}, {default_code}')
    code = int(default_code)

    if code > 600 or code < 0:
        sys.stderr.buffer.write(
            "Enum '{enum_desc.name}' range must be greater than 0 and less than or equal to 600")
        sys.exit(2)
    err_wrap = ErrorWrap(metadata=file_desc.name)
    for enum_value_desc in enum_desc.value:
        enum_code = code
        if errors_pb2.code in enum_value_desc.options.Extensions:
            enum_code = enum_value_desc.options.Extensions[errors_pb2.code]

        # If the current enumeration does not contain 'errors.code'
        # or the code value exceeds the range, the current enum will be skipped
        if enum_code > 600 or enum_code < 0:
            sys.stderr.buffer.write(
                "Enum '{enum_value_desc.name}' range must be greater than 0 and less than or equal to 600")
            sys.exit(2)
        if enum_code == 0:
            continue

        comment = ''
        # comment = v.Comments.Leading.String()
        # if comment == "":
        # comment = v.Comments.Trailing.String()

        err = ErrorInfo(
            name=enum_desc.name,
            value=enum_value_desc.name,
            camel_value=case_to_underline(enum_value_desc.name),
            http_code=enum_code,
            comment=comment,
            has_comment=len(comment) > 0)
        err_wrap.append(err)

        logger.info(err.to_json())

    if len(err_wrap) == 0:
        return ''
    return err_wrap.execute()


def case_to_underline(name: str) -> str:
    name = [i.lower() for i in name.split('_')]
    return '_'.join(name)


def case_to_camel(name: str) -> str:
    if "_" not in name:
        if name == name.upper():
            name = name.lower()

        return name.title()

    strs = name.split("_")
    words = []
    for w in strs:
        hasLower = False
        for r in w:
            if r.islower():
                hasLower = True
                break
        if not hasLower:
            w = w.lower()

        w = w.title()
        words.append(w)

    return "".join(words)
