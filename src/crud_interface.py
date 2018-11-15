from src import memory_node
from src import neo4j_label
from src import neo4j
from src import memory_interface


class CRUD(object):
    # Create a node
    @staticmethod
    def create(request: memory_node.MemoryNodeModel):
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel.other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel.none):
            return neo4j.Neo4j.create_node(request)
        return None

    # Get node by ID
    @staticmethod
    def retrieve(id_, memory: memory_interface.MemoryInterface):
        if id_ > 0:
            return neo4j.Neo4j.get_node_by_id(id_, memory)
        elif id_ == 0:
            pass
        # TODO what labels? We do not have a node do we?
        # if id == 0 returns list[memorynodemodel's where each node has the same labels,properties and relationships]
        return None

    # Update Nodes
    @staticmethod
    def update(request: memory_node.MemoryNodeModel):
        if not request.get_label().__eq__(neo4j_label.Neo4jLabel.other) and \
                not request.get_label().__eq__(neo4j_label.Neo4jLabel.none):
            return neo4j.Neo4j.update_node(request)
        return False

    # Delete a Node
    @staticmethod
    def delete(request: memory_node.MemoryNodeModel):
        if request.get_id() > 0:
            # TODO: if id != 0 and retrieve(argument) == null returns true else returns false
            return neo4j.Neo4j.delete(request)
        return False
