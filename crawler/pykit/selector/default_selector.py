
from typing import List
from typing import Tuple, Callable
from pykit.error import Error
from pykit import context
from pykit.selector import Selector, Node
from pykit.selector.balancer import Balancer, WeightedNodeBuilder

# Default is composite selector.


class DefaultSelector(Selector):
    def __init__(self, node_builder: WeightedNodeBuilder, balancer: Balancer,
                 filters: List[Callable] = None):
        self.node_builder = node_builder
        self.balancer = balancer
        self.filters = filters or []
        self.nodes = None

        # Apply update nodes info.
    def apply(self, nodes: List[Node]):
        weighted_nodes = []
        for i in nodes:
            weighted_nodes.append(self.node_builder.build(i))
        self.nodes = weighted_nodes

    # Select is select one node.
    def select(self, ctx: context.Context, filters: List[Callable]) -> Tuple[Node, Callable, Error]:

        nodes = self.nodes
        if not nodes:
            return None, None, Error()

        filters = filters or []
        filters = filters.extend(self.filters)
        new_nodes = nodes
        if filters:
            for i in filter:
                new_nodes = i(ctx, new_nodes)

        if not new_nodes:
            return None, None, Error()

        wn, done, err = self.balancer.pick(ctx, new_nodes)
        if err:
            return None, None, Error()

        return wn.Raw(), done, None
