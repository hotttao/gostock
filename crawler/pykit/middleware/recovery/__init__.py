
class Recovery:
    def __init__(self):
        pass

    def __call__(self, handler):
        def _handler(ctx, req):
            print("before recovery middleware")
            reply = handler(ctx, req)
            print("after recovery middleware")
            return reply
        return _handler
