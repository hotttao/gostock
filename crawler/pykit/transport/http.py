
class Server:
    def __init__(self) -> None:
        self.lis = None  # net.Listener
        self.endpoint = None  # *url.URL
        self.err = None  # error
        self.network = None  # string
        self.address = None  # string
        self.timeout = None  # time.Duration
        self.filters = []  # []FilterFunc
        self.ms = []  # []middleware.Middleware
        self.dec = []  # DecodeRequestFunc
        self.enc = None  # EncodeResponseFunc
        self.ene = None  # EncodeErrorFunc
        self.router = None  # *mux.Router


class Client:
    pass
