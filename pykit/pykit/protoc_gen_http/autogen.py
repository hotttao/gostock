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
from pykit.protoc_gen_http.template import MethodDetail, ServiceDetail
from pykit.protoc_gen_http.template import FileDetail, camel_case_vars
# from pykit.protoc_gen_http.utils import get_attrs
import logging

logger = logging.getLogger('proto-python-http')

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
        self.file_detail = FileDetail()

    def gen(self, omitempty: bool = True) -> plugin_pb2.CodeGeneratorResponse:
        """

        Returns:
            plugin_pb2.CodeGeneratorResponse: _description_
        """
        response = plugin_pb2.CodeGeneratorResponse()
        for proto_file in self.request.proto_file:
            service_list = proto_file.service
            if not service_list or (omitempty and not has_http_rule(service_list)):
                continue

            f = response.file.add()
            f.name = f'{os.path.splitext(proto_file.name)[0]}_pb2_http.py'
            content_list = []
            for service_proto in service_list:
                # logger.info(get_attrs(service_proto))
                # sys.stdout.write(str(get_attrs(service_proto)))
                content = self.gen_service(response=response, file_desc=proto_file,
                                           file_generate=f, service_proto=service_proto,
                                           omitempty=omitempty)
                if content:
                    content_list.append(content)
            f.content = '\n'.join(content_list)
        return response

    def gen_service(self, response: plugin_pb2.CodeGeneratorResponse,
                    file_desc: descriptor_pb2.FileDescriptorProto,
                    file_generate: plugin_pb2.CodeGeneratorResponse.File,
                    service_proto: descriptor_pb2.ServiceDescriptorProto, omitempty: bool):
        if service_proto.options.deprecated:
            comment = DeprecationComment
            self.file_detail.comment.append(comment)
        # HTTP Server.
        # service = file_desc.services_by_name[service_proto.name]
        sd = ServiceDetail(
            service_type=service_proto.name,
            service_name=service_proto.name,
            metadata=file_desc.name,
        )
        for method_desc in service_proto.method:
            if method_desc.client_streaming or method_desc.server_streaming:
                continue
            if annotations_pb2.http in method_desc.options.Extensions:
                rule = method_desc.options.Extensions[annotations_pb2.http]

                for bind in rule.additional_bindings:
                    sd.methods.append(build_http_rule(
                        file_desc, file_generate, method_desc, bind))
                sd.methods.append(build_http_rule(
                    file_desc, file_generate, method_desc, rule))
            elif not omitempty:
                path = f"/{service_proto.full_name}/{method_desc.name}"
                sd.methods.append(build_method_detail(
                    file_desc, file_generate, method_desc, "POST", path))

        service_content = ''
        if len(sd.methods) != 0:
            service_content = sd.execute()
        logger.info(sd.to_json())
        return service_content


def has_http_rule(services: List[descriptor_pb2.ServiceDescriptorProto]) -> bool:
    for service_desc in services:
        for method_desc in service_desc.method:
            if method_desc.client_streaming or method_desc.server_streaming:
                continue
            if annotations_pb2.http in method_desc.options.Extensions:
                return True

    return False


def build_http_rule(file_desc: descriptor_pb2.FileDescriptorProto,
                    file_generate: plugin_pb2.CodeGeneratorResponse.File,
                    m: descriptor_pb2.MethodDescriptorProto,
                    rule: http_pb2.HttpRule) -> MethodDetail:

    path = ''
    method = ''
    body = ''
    response_body = ''

    pattern = rule.WhichOneof('pattern')
    pattern_map = {
        'get': (rule.get, 'get'),
        'put': (rule.put, "put"),
        'post': (rule.post, "post"),
        'delete': (rule.delete, "delete"),
        'patch': (rule.patch, "patch"),
        'custom': (rule.custom.path, rule.custom.kind),
    }
    if pattern in pattern_map:
        path, method = pattern_map[pattern]

    body = rule.body
    response_body = rule.response_body
    method_detail = build_method_detail(
        file_desc, file_generate, m, method, path)
    if method in ["get", "delete"]:
        if body != "":
            sys.stderr.buffer.write(
                bytes(f"\u001B[31mWARN\u001B[m: {method} {path} body"
                      f"should not be declared.\n", encoding='utf8'))

    else:
        if body == "":
            sys.stderr.buffer.write(
                bytes(f"\u001B[31mWARN\u001B[m: {method} {path}"
                      f"does not declare a body.\n", encoding='utf8'))

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


def build_method_detail(file_desc: descriptor_pb2.FileDescriptorProto,
                        file_generate: plugin_pb2.CodeGeneratorResponse.File,
                        m: descriptor_pb2.MethodDescriptorProto,
                        method: str, path: str) -> MethodDetail:

    path_vars = build_path_vars(path)
    message_map = {
        f'.{file_desc.package}.{i.name}': i for i in file_desc.message_type}
    logger.info(f'path_vars: {path_vars}')
    logger.info(f'file_desc: {file_desc.name}-{file_desc.package}')
    # logger.info(f'message_map: {message_map}')
    for v, s in path_vars.items():
        input_type = m.input_type

        message_proto = message_map[input_type]
        fields = {i.name: i for i in message_proto.field}
        logger.info(f'fields: {fields}')
        logger.info(f'path_vars: {v}-{s}')
        logger.info(f'input_type: {input_type}')
        # if s:
        #     path = replace_path(v, s, path)

        for field in v.split("."):
            field = field.strip()
            if not field:
                continue

            if ":" in field:
                field = field.split(":")[0]

            fd = fields.get(field)
            logger.info(
                f"fd type: {fd.label == FieldDescriptor.LABEL_OPTIONAL}")
            if not fd:
                sys.stderr.buffer.write(f"\u001B[31mERROR\u001B[m: The corresponding field '{v}'"
                                        f"declaration in message could not be found in '{path}'\n")
                sys.exit(2)

            # if fd.type == FieldDescriptor.TYPE_MESSAGE:
            #     sys.stderr.buffer.write(
            #         f"\u001B[31mWARN\u001B[m: The field in path:'{v}' shouldn't be a map.\n")
            # elif fd.IsList():
            #     sys.stderr.buffer.write(
            #         f"\u001B[31mWARN\u001B[m: The field in path:'{v}' shouldn't be a list.\n")
            if fd.label == FieldDescriptor.LABEL_REPEATED:
                sys.stderr.buffer.write(
                    f"\u001B[31mWARN\u001B[m: The field in path:'{v}' shouldn't be a list/map.\n")
            elif fd.type == FieldDescriptor.TYPE_MESSAGE or fd.type == FieldDescriptor.TYPE_GROUP:
                logger.info(f"fd.type_name: {fd.type_name}-{fd.type}")
                fields = {i.name: i for i in message_map[fd.type_name].field}

    method_detail = MethodDetail(
        name=m.name,
        original_name=m.name,
        num=MethodSets[m.name],
        request=m.input_type,
        reply=m.output_type,
        path=path,
        method=method,
        has_vars=len(path_vars) > 0,
        path_vars=path_vars
    )
    MethodSets[m.name] += 1
    logger.info(method_detail.to_json())
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
        else:
            res[name] = None
    return res
