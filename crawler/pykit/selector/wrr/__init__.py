from pykit.selector.node.direct import DirectNode
from pykit.selector.default_selector import DefaultSelector


class WrrBalancer:
    pass


def NewWrr(filters):
    selector = DefaultSelector(node_builder=DirectNode, balancer=WrrBalancer(), filters=filter)
    return selector
