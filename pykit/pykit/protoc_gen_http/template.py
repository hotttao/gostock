import re
import os
import json
import autopep8
from jinja2 import Template
from typing import List

template = Template("""
import traceback
from abc import ABCMeta
from abc import abstractmethod
from flask import request
from pykit.transport import http
from pykit.context import Context
import {{ service_detail.pb2_import }} as {{ service_detail.pb2_import_as }}


class I{{ service_detail.service_name }}ServiceHTTPServer(metaclass=ABCMeta):

{% for method in service_detail.method_set %}
    @abstractmethod
    def {{ method.name }}(context: http.Context, req: {{ service_detail.pb2_import_as }}.{{ method.request }}) -> {{ service_detail.pb2_import_as }}.{{ method.reply }}:
        pass

{% endfor %}

def Register{{ service_detail.service_name }}ServiceHTTPServer(s: http.Server, srv: I{{ service_detail.service_name }}ServiceHTTPServer):
    r = s.router("/")
    {% for method in service_detail.methods %}
    r.{{ method.method }}("{{ method.path }}", _{{ service_detail.service_name }}Service_{{ method.name }}{{ method.num }}_HTTP_Handler(r, srv))
    {% endfor %}
    pass

{% for method in service_detail.methods %}
def _{{ service_detail.service_name }}Service_{{ method.name }}{{ method.num }}_HTTP_Handler(router: http.Router, srv: I{{ service_detail.service_name }}ServiceHTTPServer):
    def _{{ method.name|lower }}{{ method.num }}_hanlder(**kwargs):
        try:
            ctx = http.Context(request=request, url_params=kwargs, router=router)
            url_to_proto = {{ method.url_to_proto }}
            req = {{ service_detail.pb2_import_as }}.{{ method.request }}()
            req = ctx.bind_vars(req, url_to_proto)
            # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
            h = router.middleware(srv.{{ method.name }})
            reply = h(req, ctx)
            return ctx.result(reply)
        except Exception as e:
            traceback.print_exc(e)
            return router.srv.encoder_error(request=ctx.request, response=ctx.response, err=e)
    return _{{ method.name|lower }}{{ method.num }}_hanlder

{% endfor %}

class I{{ service_detail.service_name }}ServiceHTTPClient(metaclass=ABCMeta):
{% for method in service_detail.method_set %}
    @abstractmethod
    def {{ method.name }}(self, ctx: http.Context, req: {{ service_detail.pb2_import_as }}.{{ method.request }}, *args,
                     **kwargs) -> {{ service_detail.pb2_import_as }}.{{ method.reply }}:
        pass

{% endfor %}

class {{ service_detail.service_name }}ServiceHTTPClientImpl(I{{ service_detail.service_name }}ServiceHTTPClient):
    def __init__(self, cc: http.Client):
        self.cc = cc

{% for method in service_detail.method_set %}
    def {{ method.name }}(self, ctx: Context, req: {{ service_detail.pb2_import_as }}.{{ method.request }},
                     *args, **kwargs) -> {{ service_detail.pb2_import_as }}.{{ method.reply }}:
        pattern = "{{ method.path }}"
        url_to_proto = {{ method.url_to_proto }}
        path = http.encode_url(pattern, req, url_to_proto)
        # opts = append(opts, http.Operation("/api.stock.v1.StockInfoService/GetStockInfo"))
        # opts = append(opts, http.PathTemplate(pattern))
        out = self.cc.invoke(ctx=ctx, method="{{ method.method }}", path=path, req_pb2=req, *args, **kwargs)
        return out, None
{% endfor %}

def New{{ service_detail.service_name }}ServiceHTTPClient(client: http.Client) -> I{{ service_detail.service_name }}ServiceHTTPClient:
    return {{ service_detail.service_name }}ServiceHTTPClientImpl(client)                    

""")


class FileDetail:
    def __init__(self, comment: List[str] = None):
        self.comment = comment


class MethodDetail:
    def __init__(self, name: str, original_name: str, num: int, request: str, reply: str,
                 path: str, method: str, has_vars: bool, has_body: bool = False, body: str = '',
                 response_body: str = '', path_vars=None):
        """_summary_

            Args:
                name (str): _description_
                original_name (str): The parsed original name
                num (int): _description_
                request (str): _description_
                reply (str): _description_
                path (str): _description_
                method (str): _description_
                has_vars (bool): _description_
                has_body (bool): _description_
                body (str): _description_
                response_body (str): _description_

            Returns:
                _type_: _description_
        """
        self.name = name
        self.original_name = original_name
        self.num = num
        self.request = request.split('.')[-1] if request else ''
        self.reply = reply.split('.')[-1] if reply else ''
        self.method = method
        self.has_vars = has_vars
        self.has_body = has_body
        self.body = body
        self.response_body = response_body
        self.path_vars = path_vars or {}
        self.path, self.url_to_proto, self.proto_to_url = trans_path(
            path, self.path_vars)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

    def to_dict(self):
        return {
            'name': self.name,
            'original_name': self.original_name,
            'num': self.num,
            'request': self.request,
            'reply': self.reply,
            'path': self.path,
            'method': self.method,
            'has_vars': self.has_vars,
            'has_body': self.has_body,
            'body': self.body,
            'response_body': self.response_body,
            'path_vars': self.path_vars,
            'url_to_proto': self.url_to_proto,
            'proto_to_url': self.proto_to_url
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


class ServiceDetail:
    def __init__(self, service_type: str, service_name: str,
                 metadata: str, methods: MethodDetail = None):
        """_summary_

        Args:
            service_type (str): Greeter
            service_name (str): helloworld.Greeter
            metadata (str): api/helloworld/helloworld.proto
            methods (MethodDesc):
        """
        self.service_type = service_type
        self.service_name = service_name
        self.metadata = metadata
        self.methods = methods or []
        self.method_set = {}

    def __hash__(self) -> int:
        return hash(self.service_name)

    def __eq__(self, __o: object) -> bool:
        return self.service_name == __o.service_name

    def execute(self) -> str:
        post_set = {i for i in self.methods if i.method == 'post'}
        get_set = {i for i in self.methods if i.method == 'get'}
        get_set.update(post_set)
        self.method_set = get_set
        code = template.render(service_detail=self)
        return autopep8.fix_code(code)

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

    def to_dict(self):
        return {
            'service_type': self.service_type,
            'service_name': self.service_name,
            'metadata': self.metadata,
            # 'methods': self.methods,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


def trans_path(path, path_vars):
    """
    把 HttpRule 中定义的 url 转换成 flask 的 url 定义
    """
    proto_to_url = {}
    for proto_key, value in path_vars.items():
        url_var = proto_key
        if '.' in proto_key:
            url_var = proto_key.replace('.', '_')
            proto_to_url[proto_key] = {'url_var': url_var, 'prefix': ''}

    for proto_key, value in path_vars.items():
        if value:
            path, prefix = replace_path(proto_key, value, path)
            if prefix:
                proto_to_url[proto_key]['prefix'] = prefix

    for proto_key, var_map in proto_to_url.items():
        url_var = var_map['url_var']
        path = path.replace('{%s}' % proto_key, f'<{url_var}>')
    url_to_proto = {var_map['url_var']: {'proto_key': camel_case_vars(proto_key), 'prefix': var_map['prefix']}
                    for proto_key, var_map in proto_to_url.items()}
    return path, url_to_proto, proto_to_url


def replace_path(name: str, value: str, path: str) -> str:
    pattern = re.compile(r"(?i){([\s]*%s[\s]*)=?([^{}]*)}" % name)
    match = pattern.search(path)
    path_vars_trans = {}
    prefix = ''
    if match:
        start = match.start()
        end = match.end()
        url_var = name.replace('.', '_')
        path_vars_trans[url_var] = name
        if '/*' in value:
            # messages/* 变成 flask <path:>
            prefix = value.split('/*')[0]
            sub_path = f"{prefix}/<path:{url_var}>"
        else:

            sub_path = f"<{url_var}>"
        # new_value = value.replace("*", ".*")
        # print(path, path[start:end], prefix, sub_path)
        path = path.replace(path[start:end], f'{sub_path}')
    return path, prefix


def camel_case_vars(s: str):
    subs = s.split(".")
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
    first = True
    for i in s.split("_"):
        if not i:
            continue
        if i[0].isdigit():
            stub = f'_{i}'
        else:
            if first:
                first = False
                stub = i
            else:
                stub = i.capitalize()
        stubs.append(stub)
    return ''.join(stubs)