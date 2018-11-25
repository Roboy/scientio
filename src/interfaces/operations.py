from abc import ABC, abstractmethod

from src.node_model import NodeModel


class Operations(ABC):
    """
    Interface for CRUD operations within a graph memory
    """
    @staticmethod
    @abstractmethod
    def create(request: NodeModel) -> NodeModel:
        """
        Create a node
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def retrieve(request: NodeModel, node_id: int = None) -> NodeModel:
        """
        Get node by ID
        :param request:
        :param node_id:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def update(request: NodeModel) -> NodeModel:
        """
        Update Nodes
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def delete(request: NodeModel) -> bool:
        """
        Delete a Node
        :param request:
        :return: bool
        """
        return NotImplemented
