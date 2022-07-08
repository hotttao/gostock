
from typing import List, Tuple
from typing import Callable
from pykit.error import Error
from pykit import context
from pykit.selector import balancer
from pykit.selector.node.direct import DirectNode
from pykit.selector.default_selector import DefaultSelector
from pykit.selector.balancer import WeightedNode


class WrrBalancer(balancer.Balancer):
    def __init__(self):
        self.current_weight = {}

    def pick(self, ctx: context.Context, nodes: List[WeightedNode]) -> Tuple[WeightedNode, Callable, Error]:
        if not nodes:
            return None, None, Error()

        total_weight = 0
        selected = None
        select_weight = 0

        # nginx wrr load balancing algorithm: http://blog.csdn.net/zhangskd/article/details/50194069
        # p.mu.Lock()
        for node in nodes:
            total_weight += node.weight
            cwt = self.current_weight.get(node.address, 0)
            cwt += node.weight
            self.current_weight[node.address] = cwt
            if not selected or select_weight < cwt:
                select_weight = cwt
                selected = node

        self.currentWeight[selected.address] = select_weight - total_weight
        # p.mu.Unlock()

        d = selected.Pick()
        return selected, d, None


def NewWrr(filters=None):
    selector = DefaultSelector(node_builder=DirectNode, balancer=WrrBalancer(), filters=filters)
    return selector
