from abc import ABCMeta, abstractmethod
from typing import Tuple
from typing import List
from typing import Callable
from pykit.error import Error
from pykit import context
from pykit.selector import Node


# WeightedNode calculates scheduling weight in real time
class WeightedNode(Node):

    # Raw returns the original node
    @abstractmethod
    def raw() -> Node:
        pass

    # Weight is the runtime calculated weight@abstractmethod
    @property
    @abstractmethod
    def weight() -> float:
        pass

    # Pick the node@abstractmethod
    def pick() -> Callable:
        pass

    # PickElapsed is time elapsed since the latest pick
    @abstractmethod
    def pick_elapsed() -> int:
        pass


class Balancer(metaclass=ABCMeta):
    # Balancer is balancer interface
    @abstractmethod
    def pick(ctx: context.Context, nodes: List[WeightedNode]) -> Tuple[WeightedNode, Callable, Error]:
        pass


# WeightedNodeBuilder is WeightedNode Builder
class WeightedNodeBuilder:
    def build(Node) -> WeightedNode:
        pass
