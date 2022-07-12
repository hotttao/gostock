
from typing import List, Callable


class Middleware:
    pass


def Chain(m: List[Callable]) -> Callable:
    def _handler(next: Callable) -> Callable:
        i = len(m) - 1
        while i >= 0:
            next = m[i](next)
            i -= 1
        return next
    return _handler
