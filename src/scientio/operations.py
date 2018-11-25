from abc import ABC, abstractmethod
from src.scientio.memory_node_model import MemoryNodeModel


class Operations(ABC):
    """
    Interface for CRUD operations within a graph memory
    """
    @abstractmethod
    def create(self, request: MemoryNodeModel) -> MemoryNodeModel:
        """
        Create a node
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @abstractmethod
    def retrieve(self, request: MemoryNodeModel, node_id: int = None) -> MemoryNodeModel:
        """
        Get node by ID
        :param request:
        :param node_id:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @abstractmethod
    def update(self, request: MemoryNodeModel) -> MemoryNodeModel:
        """
        Update Nodes
        :param request:
        :return: MemoryNodeModel
        """
        return NotImplemented

    @abstractmethod
    def delete(self, request: MemoryNodeModel) -> bool:
        """
        Delete a Node
        :param request:
        :return: bool
        """
        return NotImplemented
