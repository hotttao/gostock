import json
from pykit.encoding import Codec
from pykit.encoding import register_codec


class JsonCodec(Codec):
    name = "json"

    def marshal(self, v):
        return json.dumps(v)

    def unmarshal(self, data):
        return json.loads(data)


register_codec(JsonCodec)
