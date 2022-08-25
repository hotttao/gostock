import json
import os
import autopep8
from jinja2 import Template
from typing import List

template = Template("""
                    
from abc import ABCMeta
from abc import abstractmethod
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
    def _{{ method.name|lower }}_hanlder(ctx: http.Context):
        req = {{ service_detail.pb2_import_as }}.{{ method.request }}()
        req = ctx.bind_vars(req)
        # http.SetOperation(ctx, "/api.stock.v1.StockInfoService/GetStockInfo")
        h = router.middleware(srv.{{ method.name }})
        reply = h(req, ctx)
        return ctx.result(reply)
    return _{{ method.name|lower }}_hanlder

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
        path = http.encode_url(pattern, req)
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
                 response_body: str = ''):
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
        self.path = path
        self.method = method
        self.has_vars = has_vars
        self.has_body = has_body
        self.body = body
        self.response_body = response_body

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
        post_set.update(get_set)
        self.method_set = post_set
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
