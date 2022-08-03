
import requests
from typing import Any, List
from urllib import parse
from pykit import context

from pykit.selector import Selector
from pykit.selector import wrr, DoneInfo
from pykit.registry import Discovery
from pykit.middleware import Middleware, Chain
from pykit.transport.http import resolver
from pykit.transport.http import codec
from pykit.transport.http.transport import Transport
from pykit.transport import new_client_context


def encode_url(url):
    pass


class Client:
    def __init__(self, endpoint: str, user_agent: str = '',
                 response_decoder=None, request_encoder=None, error_decoder=None,
                 timeout: int = 2, block: bool = False, transport=None, selector: Selector = None,
                 discovery: Discovery = None, middlewares: List[Middleware] = None):
        self.ctx = None
        self.err = None  # error
        self.timeout = timeout  # time.Duration
        self.endpoint = endpoint
        self.user_agent = user_agent

        self.request_encoder = request_encoder or codec.default_request_encoder  # EncodeRequestdef
        self.response_decoder = response_decoder or codec.default_response_decoder  # DecodeResponsedef
        self.error_decoder = error_decoder or codec.default_error_decoder  # DecodeErrordef

        self.selector = selector or wrr.NewWrr()  # selector.Selector
        self.discovery = discovery  # registry.Discovery
        self.middlewares = middlewares or []  # []middleware.Middleware
        self.block = block

        self.target = parse.urlparse(endpoint)  # Target

        self.transport = transport
        self.r = self.get_resolver()       # resolver

        self.cc = requests.Session()

    def get_resolver(self):
        self.insecure = True
        if not self.discovery:
            return None
        print(self.target)
        if self.target.scheme == "discovery":
            r = resolver.Resolver(self.ctx, self.discovery, self.target,
                                  self.selector, self.block, self.insecure)
            # return nil, fmt.Errorf("[http client] new resolver failed!err: %v", options.endpoint)
            return r

    def close(self):
        # Close tears down the Transport and all underlying connections.
        if self.cc:
            return self.cc.close()

    def invoke(self, ctx: context.Context, method: str, path: str, req_pb2: Any, **kwargs):
        # Invoke makes an rpc call procedure for remote service.
        # c = defaultCallInfo(path)
        # for _, o = range opts:
        #     if err = o.before(& c); err:
        #         return err

        if req_pb2:
            content_type = kwargs.get('content_type', "application/json")
            data = self.request_encoder(content_type, req_pb2)
            # print(data)

        url = f"{self.target.scheme}://{self.target.netloc}{path}"
        # print(url)
        req_obj = requests.Request(method=method, url=url, json=data)

        if content_type:
            req_obj.headers["Content-Type"] = content_type

        if self.user_agent:
            req_obj.headers["User-Agent"] = self.user_agent

        ctx = new_client_context(ctx, Transport(
            endpoint=self.endpoint,
            request_header=req_obj.headers,
            operation=path,
            request=req_obj,
            path_template=path
        ))
        return self._invoke(ctx, req_obj, req_pb2, **kwargs)

    def _invoke(self, ctx: context.Context, req: requests.Request, req_pb2: Any, **kwargs):
        def h(ctx: context.Context, in_param: Any):
            res = self.do(req)
            # if res != nil:
            #     cs = csAttempt{res: res
            #     for _, o = range opts:
            #         o.after(& c, & cs)
            reply = self.response_decoder(res)
            print(reply)
            return reply

        if self.middlewares:
            h = Chain(self.middlewares)(h)

        return h(ctx, req_pb2)

    def do(self, req: requests.Request, **kwargs) -> requests.Response:
        # Do send an HTTP request and decodes the body of response into target.
        # returns an error (of type *Error) if the response status code is not 2xx.
        # c = defaultCallInfo(req.URL.Path)
        # for _, o = range opts:
        # if err = o.before( & c); err:
        # return nil, err

        return self._do(req)

    def _do(self, req: requests.Request) -> requests.Response:
        # done = DoneInfo()
        done = None
        if self.r:
            node, done, err = self.selector.select(self.ctx)
            print(node)

            if self.insecure:
                scheme = "http"
            else:
                scheme = "https"
            target = parse.urlparse(req.url)
            endpoint = parse.ParseResult(scheme=scheme, netloc=node.address, query=target.query,
                                         path=target.path, params=target.params, fragment=target.fragment)
            url = endpoint.geturl()
            print(url)
            req.url = url
        prepped = req.prepare()
        resp = self.cc.send(prepped)
        # err = self.error_decoder(resp)
        # if done:
        # done(req, DoneInfo(err))

        return resp
