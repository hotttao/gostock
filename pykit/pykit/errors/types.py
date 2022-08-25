
from pykit.errors import Error


def service_unavailable(reason: str, message: str) -> Error:
    return Error(503, reason, message)


ErrNoAvailable = service_unavailable("no_available_node", "")
