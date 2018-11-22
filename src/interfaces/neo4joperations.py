# I'm a stub for the neo4j connection
from typing import Optional

from src import neo4j_label

# Probably Neo4j methods can be all static ...
from src.interfaces.operations import Operations
from src.memory_node_model import MemoryNodeModel
from src.neo4j import Neo4j


class Neo4jOperations(Operations):
    """
    Implementation of the operations interface for a Neo4j-based graph memory
    """
    # Create a node
    @staticmethod
    def create(request: MemoryNodeModel) -> Optional[MemoryNodeModel]:
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
            return Neo4j().create_node(request)
        return None

    # Get node by ID
    @staticmethod
    def retrieve(request: MemoryNodeModel, node_id: int = None) -> Optional[MemoryNodeModel]:
        if node_id is not None and node_id >= 0:
            return Neo4j().get_node_by_id(node_id)
        elif node_id is None:
            if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                    not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
                return Neo4j().get_node(request)
        return None

    # Update Nodes
    @staticmethod
    def update(request: MemoryNodeModel) -> Optional[MemoryNodeModel]:
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
            return Neo4j().update_node(request)
        return None

    # Delete a Node
    @staticmethod
    def delete(request: MemoryNodeModel) -> bool:
        if request.get_id() > 0 and Neo4jOperations.retrieve(request, request.get_id()) is not None:
            Neo4j().delete_node(request)
            return True
        return False

