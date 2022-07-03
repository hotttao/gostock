from abc import ABCMeta, abstractmethod
from typing import Any


class Codec(metaclass=ABCMeta):
    @abstractmethod
    def marshal(v: Any) -> str:
        pass

    @abstractmethod
    def unmarshal(data: str) -> str:
        pass

    @abstractmethod
    def name() -> str:
        pass


registeredCodecs = {}


def register_codec(codec: Codec):
    if codec:
        raise ValueError("cannot register a nil Codec")

    if not codec.Name():
        raise ValueError("cannot register Codec with empty string result for Name()")

    content_subtype = codec.Name().lower()
    registeredCodecs[content_subtype] = codec


def get_codec(content_subtype: str) -> Codec:
    return registeredCodecs[content_subtype]
