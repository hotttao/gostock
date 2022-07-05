
from typing import Dict
from pykit.selector import Node
from pykit.registry import ServiceInstance


class DefaultNode(Node):
    # DefaultNode is selector node
    def __init__(self, scheme: str, address: str, weight: int = 0, version: str = '',
                 name: str = '', metadata: Dict[str, str] = None):
        self.scheme = scheme
        self.address = address
        self.weight = weight
        self.version = version
        self.name = name
        self.metadata = metadata or {}

    @property
    def initial_weight(self) -> int:
        return self.weight

    @classmethod
    def build(cls, schema: str, address: str, instance: ServiceInstance):
        """_summary_

        Args:
            schema (str): _description_
            address (str): _description_
            instance (ServiceInstance): _description_
        """
        node = cls(schema, address)
        if instance:
            node.name = instance.name
            node.version = instance.version
            node.metadata = instance.metadata
            if 'weight' in node.metadata:
                node.weight = float(node.metadata['weight'])
        return node
