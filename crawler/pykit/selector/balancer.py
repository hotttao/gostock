from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from pykit.error import Error
from pykit import context
from pykit.selector import Node, DoneFunc


# WeightedNode calculates scheduling weight in real time
class WeightedNode(Node):

    # Raw returns the original node
    @abstractmethod
    def Raw() -> Node:
        pass

    # Weight is the runtime calculated weight@abstractmethod
    def Weight() -> float:
        pass

    # Pick the node@abstractmethod
    def Pick() -> DoneFunc:
        pass

    # PickElapsed is time elapsed since the latest pick
    @abstractmethod
    def pick_elapsed() -> int:
        pass


class Balancer(metaclass=ABCMeta):
    # Balancer is balancer interface
    @abstractmethod
    def pick(ctx: context.Context, nodes: List[WeightedNode]) -> Tuple[WeightedNode, DoneFunc, Error]:
        pass


# WeightedNodeBuilder is WeightedNode Builder
class WeightedNodeBuilder:
    def build(Node) -> WeightedNode:
        pass
