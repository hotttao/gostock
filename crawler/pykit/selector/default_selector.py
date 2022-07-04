
from typing import List
from typing import Tuple
from pykit.error import Error
from pykit import context
from pykit.selector import Filter, Selector, DoneFunc, Node
from pykit.selector.balancer import Balancer, WeightedNodeBuilder

# Default is composite selector.


class DefaultSelector(Selector):
    def __init__(self, node_builder: WeightedNodeBuilder, balancer: Balancer,
                 filters: List[Filter]):
        self.node_builder = node_builder
        self.balancer = balancer
        self.filters = filters
        self.nodes = None

        # Apply update nodes info.
    def apply(self, nodes: List[Node]):
        weighted_nodes = []
        for i in nodes:
            weighted_nodes.append(self.node_builder.build(i))
        self.nodes = weighted_nodes

    # Select is select one node.
    def select(self, ctx: context.Context, filters: List[Filter]) -> Tuple[Node, DoneFunc, Error]:

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
