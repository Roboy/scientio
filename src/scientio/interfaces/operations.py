from abc import ABC, abstractmethod
from scientio.node_model import NodeModel


class Operations(ABC):
    """
    Interface for CRUD operations within a graph memory
    """
    @abstractmethod
    def create(self, request: NodeModel) -> NodeModel:
        """
        Create a node
        :param request:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def retrieve(self, request: NodeModel, node_id: int = None) -> NodeModel:
        """
        Get node by ID
        :param request:
        :param node_id:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def update(self, request: NodeModel) -> NodeModel:
        """
        Update Nodes
        :param request:
        :return: NodeModel
        """
        return NotImplemented

    @abstractmethod
    def delete(self, request: NodeModel) -> bool:
        """
        Delete a Node
        :param request:
        :return: bool
        """
        return NotImplemented
