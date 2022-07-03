

def encode_url(url):
    pass


class Client:
    def __init__(self,):
        self.err = None  # error
        self.network = None  # string
        self.address = None  # string
        self.timeout = None  # time.Duration
        self.filters = []  # []FilterFunc
        self.ms = []  # []middleware.Middleware
        self.dec = []  # DecodeRequestFunc
        self.enc = None  # EncodeResponseFunc
        self.ene = None  # EncodeErrorFunc
