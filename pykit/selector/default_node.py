import json
from typing import Dict
from pykit.selector import Node
from pykit.registry import ServiceInstance


class DefaultNode(Node):
    scheme = ''
    address = ''
    weight = 0
    version = 'version'
    service_name = ''
    metadata = None

    def __init__(self, scheme: str, address: str, weight: int = 0, version: str = '',
                 service_name: str = '', metadata: Dict[str, str] = None):
        self.scheme = scheme
        self.address = address
        self.weight = weight
        self.version = version
        self.service_name = service_name
        self.metadata = metadata or {}

    @property
    def initial_weight(self) -> int:
        return self.weight

    def to_dict(self):
        return {
            'scheme': self.scheme,
            'address': self.address,
            'weight': self.weight,
            'version': self.version,
            'service_name': self.service_name
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    __repr__ = __str__

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
            node.service_name = instance.name
            node.version = instance.version
            node.metadata = instance.metadata
            if 'weight' in node.metadata:
                node.weight = float(node.metadata['weight'])
        return node
