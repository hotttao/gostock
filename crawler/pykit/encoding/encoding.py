from abc import ABCMeta, abstractmethod

registered_codecs = {}


class Codec(metaclass=ABCMeta):

    @abstractmethod
    def marshal(v):
        # Marshal returns the wire format of v.
        pass

    @abstractmethod
    def unmarshal(data):
        # Unmarshal parses the wire format into v.
        pass

    @property
    @abstractmethod
    def name() -> str:
        # Name returns the name of the Codec implementation. The returned string
        # will be used as part of content type in transmission.  The result must be
        # static; the result cannot change between calls.
        pass


# RegisterCodec registers the provided Codec for use with all Transport clients and
# servers.
def register_codec(codec: Codec):
    if not codec:
        raise ValueError("cannot register a nil Codec")

    if not codec.name:
        raise ValueError("cannot register Codec with empty string result for Name()")

    content_subtype = codec.name.lower()
    registered_codecs[content_subtype] = codec


def get_codec(content_subtype: str) -> Codec:
    # GetCodec gets a registered Codec by content-subtype, or nil if no Codec is
    # registered for the content-subtype.
    #
    # The content-subtype is expected to be lowercase.
    return registered_codecs.get_codec(content_subtype.lower())
