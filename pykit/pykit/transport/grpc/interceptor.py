import grpc
from typing import Callable, Any
from grpc_interceptor import ServerInterceptor
from grpc_interceptor import ClientInterceptor
from grpc_interceptor.exceptions import GrpcException
from pykit import middleware


class ServerInterceptorWrapt(ServerInterceptor):

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
        handler = self.trans_middleware(method)
        try:
            response_or_iterator = handler(request, context)
        except GrpcException as e:
            # If it was unary, then any exception raised would be caught
            # immediately, so handle it here.
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
        # Check if it's streaming
        if hasattr(response_or_iterator, "__iter__"):
            # Now we know it's a server streaming RPC, so the actual RPC method
            # hasn't run yet. Delegate to a helper to iterate over it so it runs.
            # The helper needs to re-yield the responses, and we need to return
            # the generator that produces.
            return self._intercept_streaming(response_or_iterator, context)
        else:
            # For unary cases, we are done, so just return the response.
            return response_or_iterator

    def _intercept_streaming(self, iterator, context):
        try:
            for resp in iterator:
                yield resp
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise


class ClientInterceptorWrapt(ClientInterceptor):
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
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        handler = self.trans_middleware(method)
        return handler(request_or_iterator, call_details)
