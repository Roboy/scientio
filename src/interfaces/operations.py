from abc import ABC, abstractmethod

from src.memory_node_model import MemoryNodeModel


class Operations(ABC):
    """
    Interface for CRUD operations within a graph memory
    """
    @staticmethod
    @abstractmethod
    def create(request: MemoryNodeModel) -> MemoryNodeModel:
        """
        Create a node
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def retrieve(request: MemoryNodeModel, node_id: int = None) -> MemoryNodeModel:
        """
        Get node by ID
        :param request:
        :param node_id:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def update(request: MemoryNodeModel) -> MemoryNodeModel:
        """
        Update Nodes
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def delete(request: MemoryNodeModel) -> bool:
        """
        Delete a Node
        :param request:
        :return: bool
        """
        return NotImplemented
