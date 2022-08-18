import json
from pykit.encoding import Codec
from pykit.encoding import register_codec
from google.protobuf.json_format import MessageToDict


class JsonCodec(Codec):
    name = "json"

    def marshal(self, v):
        v = MessageToDict(v)
        return json.dumps(v)

    def unmarshal(self, data):
        return json.loads(data)


register_codec(JsonCodec)
