import grpc
from typing import Callable, Any
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from pykit import middleware


class MiddlewareInterceptor(ServerInterceptor):

    def __init__(self, middlewares=None):
        self.middlewares = middlewares

    def trans_middleware(self, method):
        # md, _ := grpcmd.FromIncomingContext(ctx)
        # replyHeader := grpcmd.MD{}
        # ctx = transport.NewServerContext(ctx, &Transport{
        # 	endpoint:    s.endpoint.String(),
        # 	operation:   info.FullMethod,
        # 	reqHeader:   headerCarrier(md),
        # 	replyHeader: headerCarrier(replyHeader),
        # })
        if self.middlewares:
            h = middleware.Chain(self.middlewares)(method)
        return h

    def intercept(
        self,
        method: Callable,
        request: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        """Override this method to implement a custom interceptor.

         You should call method(request, context) to invoke the
         next handler (either the RPC method implementation, or the
         next interceptor in the list).

         Args:
             method: The next interceptor, or method implementation.
             request: The RPC request, as a protobuf message.
             context: The ServicerContext pass by gRPC to the service.
             method_name: A string of the form
                 "/protobuf.package.Service/Method"

         Returns:
             This should generally return the result of
             method(request, context), which is typically the RPC
             method response, as a protobuf message. The interceptor
             is free to modify this in some way, however.
         """
        try:
            print('before interceptor')
            handler = self.trans_middleware(method)
            reply = handler(request, context)
            print('afeter interceptor')
            print(reply)
            return reply
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
