from src import memory_node
from src import memory_interface
from src import neo4j_label
from src import neo4j


class CRUD(object):
    # Create a node
    @staticmethod
    def create(request: memory_node.MemoryNodeModel):
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
            return neo4j.Neo4j().create_node(request)
        return None

    # Get node by ID
    @staticmethod
    def retrieve(request: memory_node.MemoryNodeModel, node_id, memory: memory_interface.MemoryInterface):
        if node_id > 0:
            return neo4j.Neo4j().get_node_by_id(node_id, memory)
        elif node_id == 0:
            if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                    not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
                return neo4j.Neo4j().get_node(request, memory)
        return None

    # Update Nodes
    @staticmethod
    def update(request: memory_node.MemoryNodeModel):
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel().other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel().none):
            return neo4j.Neo4j().update_node(request)
        return False

    # Delete a Node
    @staticmethod
    def delete(request: memory_node.MemoryNodeModel, memory: memory_interface.MemoryInterface):
        if request.get_id() > 0 and CRUD.retrieve(request, request.get_id(), memory) is not None:
            neo4j.Neo4j().delete(request)
            return True
        return False
