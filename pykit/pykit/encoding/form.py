import json
from pykit.encoding import Codec
from pykit.encoding import register_codec
from google.protobuf.json_format import MessageToDict


class FormCodec(Codec):
    name = "x-www-form-urlencoded"

    def marshal(self, v):
        v = MessageToDict(v)
        return json.dumps(v)

    def unmarshal(self, data):
        return ''


register_codec(FormCodec)
