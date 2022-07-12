
class Recovery:
    def __init__(self):
        pass

    def __call__(self, handler):
        def _handler(ctx, req):
            try:
                print("before recovery middleware")
                reply = handler(ctx, req)
                print("after recovery middleware")
                return reply
            except Exception:
                pass
        return _handler
