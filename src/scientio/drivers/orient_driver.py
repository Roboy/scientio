from typing import List

from ..interfaces.operations import Operations
from ..ontology.node import Node


class OrientDBDriver(Operations):

    def create(self, request: Node) -> Node:
        pass

    def retrieve(self, request: Node = None, node_id: int = None) -> List[Node]:
        pass

    def update(self, request: Node) -> Node:
        pass

    def delete(self, request: Node) -> bool:
        pass
