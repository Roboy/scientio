from abc import ABC, abstractmethod

from src.scientio.ontology.node import Node


class Operations(ABC):
    """
    Interface for CRUD operations within a graph memory
    """
    @abstractmethod
    def create(self, request: Node) -> Node:
        """
        Create a node
        :param request:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def retrieve(self, request: Node, node_id: int = None) -> Node:
        """
        Get node by ID
        :param request:
        :param node_id:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def update(self, request: Node) -> Node:
        """
        Update Nodes
        :param request:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def delete(self, request: Node) -> bool:
        """
        Delete a Node
        :param request:
        :return: bool
        """
        return NotImplemented
