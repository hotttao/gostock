
import time
from pykit import selector


class DirectNode:
    def __init__(self, node: selector.Node, last_pick: int):
        """_summary_

        Args:
            node (Node): _description_
            last_pick (int): last lastPick timestamp

        Returns:
            _type_: _description_
        """
        self.scheme = node.scheme
        self.address = node.address
        self.weight = node.weight or 100
        self.version = node.version
        self.name = node.name
        self.metadata = node.metadata
        self.last_pick = last_pick
        self.node = node

    def pick(self) -> selector.DoneFunc:
        now = int(time.time())
        self.last_pick = now
        return None

    def pick_elapsed(self) -> int:
        return int(time.time()) - self.last_pick

    def raw(self) -> selector.Node:
        return self.Node