import re
import os
import sys
from typing import List, Dict
from collections import defaultdict
from google.protobuf.compiler import plugin_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import type_pb2
from google.api import annotations_pb2
from google.api import http_pb2
from google.protobuf.descriptor import FieldDescriptor
from pykit.protoc_gen_http.template import MethodDetail, ServiceDetail


DeprecationComment = "// Deprecated: Do not use."
MethodSets = defaultdict(lambda: 0)


class AutoGen:
    """ Autogenerator for the MAVSDK bindings """

    def __init__(self, request: plugin_pb2.CodeGeneratorRequest):
        """_summary_

        Args:
            request (plugin_pb2.CodeGeneratorRequest): _description_
        """
        self.request = request

    def gen(self) -> plugin_pb2.CodeGeneratorResponse:
        """

        Returns:
            plugin_pb2.CodeGeneratorResponse: _description_
        """
        response = plugin_pb2.CodeGeneratorResponse()
        for proto_file in self.request.proto_file:
            service = proto_file.service

            f = response.file.add()
            f.name = f'{os.path.splitext(proto_file.name)[0]}_pb2_http.py'
            self.gen_service(response, proto_file, f, service)
            # f.content = 'import json'
        return response

    def gen_service(self, response: plugin_pb2.CodeGeneratorResponse,
                    file_desc: descriptor_pb2.FileDescriptorProto,
                    file_generate: plugin_pb2.CodeGeneratorResponse.File,
                    service: descriptor_pb2.ServiceDescriptorProto, omitempty: bool):
        if service.options.deprecated:
            comment = DeprecationComment
        # HTTP Server.
        sd = ServiceDetail(
            service_type=service.name,
            service_name=service.full_name,
            metadata=file_desc.name,
        )
        for method_desc in service.method:
            if method_desc.client_streaming or method_desc.server_streaming:
                continue
            if annotations_pb2.http in method_desc.options.Extensions:
                rule = method_desc.options.Extensions[annotations_pb2.http]

                for bind in rule.additional_bindings:
                    sd.methods.append(
                        self.build_http_rule(file_desc, file_generate, method_desc, bind))
                sd.methods.append(self.build_http_rule(
                    file_desc, file_generate, method_desc, bind))
            elif not omitempty:
                path = f"/{service.full_name}/{method_desc.name}"
                sd.methods.append(self.build_method_detail(
                    file_desc, file_generate, method_desc, "POST", path))

        if len(sd.Methods) != 0:
            content = sd.execute()
            return content

    def has_http_rule(self, services: List[descriptor_pb2.ServiceDescriptorProto]) -> bool:
        for service_desc in services:
            for method_desc in service_desc.method:
                if method_desc.client_streaming or method_desc.server_streaming:
                    continue
                if annotations_pb2.http in method_desc.options.Extensions:
                    return True

        return False

    def build_http_rule(self, file_desc: descriptor_pb2.FileDescriptorProto,
                        file_generate: plugin_pb2.CodeGeneratorResponse.File,
                        m: descriptor_pb2.MethodDescriptorProto,
                        rule: http_pb2.HttpRule) -> MethodDetail:

        path = ''
        method = ''
        body = ''
        response_body = ''

        pattern = rule.WhichOneof('pattern')
        pattern_map = {
            'get': (rule.get, 'GET'),
            'put': (rule.put, "PUT"),
            'post': (rule.post, "POST"),
            'delete': (rule.delete, "DELETE"),
            'patch': (rule.patch, "PATCH"),
            'custom': (rule.custom.path, rule.custom.kind),
        }
        if pattern in pattern_map:
            path, method = pattern_map[pattern]

        body = rule.Body
        response_body = rule.response_body
        method_detail = self.build_method_detail(
            file_desc, file_generate, m, method, path)
        if method in ["GET", "DELETE"]:
            if body != "":
                sys.stderr.buffer.write(
                    f"\u001B[31mWARN\u001B[m: {method} {path} body should not be declared.\n")

        else:
            if body == "":
                sys.stderr.buffer.write(
                    f"\u001B[31mWARN\u001B[m: {method} {path} does not declare a body.\n")

        if body == "*":
            method_detail.has_body = True
            method_detail.body = ""
        elif body != "":
            method_detail.has_body = True
            method_detail.body = "." + camel_case_vars(body)
        else:
            method_detail.has_body = False

        if response_body == "*":
            method_detail.response_body = ""
        elif response_body != "":
            method_detail.response_body = "." + \
                camel_case_vars(response_body)

        return method_detail

    def build_method_detail(self, file_desc: descriptor_pb2.FileDescriptorProto,
                            file_generate: plugin_pb2.CodeGeneratorResponse.File,
                            m: descriptor_pb2.MethodDescriptorProto,
                            method: str, path: str) -> MethodDetail:

        path_vars = build_path_vars(path)

        for v, s in path_vars.items():
            input_type = m.input_type
            message_type = file_desc.message_types_by_name[input_type]
            fields = message_type.fields_by_name
            if s:
                path = replace_path(v, s, path)

            for field in v.split("."):
                field = field.trim()
                if not field:
                    continue

                if ":" in field:
                    field = field.split(":")[0]

                fd = fields.get(field)
                if not fd:
                    sys.stderr.buffer.write(f"\u001B[31mERROR\u001B[m: The corresponding field '{v}'"
                                            f"declaration in message could not be found in '{path}'\n")
                    sys.exit(2)

                if fd.type == FieldDescriptor.TYPE_MESSAGE:
                    sys.stderr.buffer.write(
                        f"\u001B[31mWARN\u001B[m: The field in path:'{v}' shouldn't be a map.\n")
                elif fd.IsList():
                    sys.stderr.buffer.write(
                        f"\u001B[31mWARN\u001B[m: The field in path:'{v}' shouldn't be a list.\n")
                elif fd.type == FieldDescriptor.TYPE_MESSAGE or fd.type == FieldDescriptor.TYPE_MESSAGE:
                    fields = fd.Message().Fields()

        method_detail = MethodDetail(
            name=m.name,
            original_name=str(m.Desc.Name()),
            num=MethodSets[m.name],
            request=file_generate.QualifiedGoIdent(m.Input.GoIdent),
            reply=file_generate.QualifiedGoIdent(m.Output.GoIdent),
            path=path,
            method=method,
            has_vars=len(path_vars) > 0
        )
        MethodSets[m.name] += 1
        return method_detail


def build_path_vars(path: str) -> Dict[str, str]:
    if path.endswith("/"):
        sys.stderr.buffer.write(
            f"\u001B[31mWARN\u001B[m: Path {path} should not end with \"/\" \n")
    res = {}
    pattern = re.compile("(?i){([a-z\.0-9_\s]*)=?([^{}]*)}")
    matches = pattern.findall(path, -1)
    for name, value in matches:
        name = name.strip()
        if name and value:
            res[name] = value
            res[name] = None
    return res


def replace_path(name: str, value: str, path: str) -> str:
    pattern = re.compile(r"(?i){([\s]*%s[\s]*)=?([^{}]*)}" % name)
    match = pattern.search(path)
    if match:
        start = match.start()
        end = match.end()
        new_value = value.replace("*", ".*")
        path = path.replace(path[start:end], f'{name}:{new_value}')
    return path


def camel_case_vars(s: str):
    subs = s.split(s, ".")
    case_vars = [camel_case(sub) for sub in subs]
    return '.'.join(case_vars)


def camel_case(s: str) -> str:
    # camelCase返回CamelCased名称。如果有一个内部下划线和一个小写字母，删除下划线并转换为大写字母。
    # 这种重写导致名称冲突的可能性很小，但由于太过遥远，我们准备假装它不存在—因为c++生成器的名称是小写的，
    # 所以极不可能有两个大写不同的字段。简而言之，_my_field_name_2变成了XMyFieldName_2。

    if s == "":
        return ""
    # 不变量:如果下一个字母是小写，它必须转换为大写。
    # 也就是说，我们一次处理一个单词，其中单词用_或大写字母标记。数字被视为单词。
    stubs = []
    for i in s.split("_"):
        if not i:
            continue
        if i[0].isdigit():
            stub = f'_{i}'
        else:
            stub = i.capitalize()
        stubs.append(stub)
    return ''.join(stubs)
