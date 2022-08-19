from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List, Tuple
# from pykit.errors import Error
from pykit import context

# Node is node(metaclass=ABCMeta).

# ReplyMeta is Reply Metadata.


class ReplyMeta(metaclass=ABCMeta):
    @abstractmethod
    def get(key: str) -> str:
        pass


class Node(metaclass=ABCMeta):
    # Scheme is service node scheme
    @property
    @abstractmethod
    def scheme() -> str:
        pass

    # Address is the unique address under the same service
    @property
    @abstractmethod
    def address() -> str:
        pass

    # ServiceName is service name
    @property
    @abstractmethod
    def service_name() -> str:
        pass

    # InitialWeight is the initial value of scheduling weight
    # if not set return nil
    @property
    @abstractmethod
    def initial_weight() -> int:
        pass

    # Version is service node version
    @property
    @abstractmethod
    def version() -> str:
        pass

    # Metadata is the kv pair metadata associated with the service instance.
    # version,namespace,region,protocol etc..
    @property
    @abstractmethod
    def metadata() -> Dict[str, str]:
        pass


# DoneInfo is callback info when RPC invoke done.
class DoneInfo:
    def __init__(self, error, reply_meta: ReplyMeta, bytes_sent: bool, bytes_received: bool):
        """_summary_

        Args:
            error (Error): Response Error
            reply_meta (ReplyMeta): Response Metadata
            bytes_sent (bool): BytesSent indicates if any bytes have been sent to the server.
            bytes_received (bool): BytesReceived indicates if any byte has been received from the server.
        """
        self.error = error
        self.reply_meta = reply_meta
        self.bytes_sent = bytes_sent
        self.bytes_received = bytes_received


# Rebalancer is nodes rebalancer.
class Rebalancer(metaclass=ABCMeta):
    # Apply is apply all nodes when any changes happen
    def apply(nodes: List[Node]):
        pass


# Filter: Callable[[context.Context, List[Node]], List[Node]] = None
# DoneFunc: Callable[[context.Context, DoneInfo]] = None


class Selector(Rebalancer):
    # Selector is node pick balancer.

    # Select nodes
    # if err == nil, selected and done must not be empty.
    @abstractmethod
    def select(ctx: context.Context, filters: List[Callable]) -> Tuple[Node, Callable]:
        pass


# Builder build selector
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def build() -> Selector:
        pass
