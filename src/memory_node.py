from src import node
from src import memory_interface
from src import neo4j_relationship
from src import neo4j_property


class MemoryNodeModel(node.NodeModel):

    def __init__(self, memory: memory_interface.MemoryInterface=None,
                 memory_node=None, strip_query=None):
        super().__init__(self)
        # GSON stuff: @Expose: private transient boolean stripQuery
        self.strip_query = False
        if memory:
            self.memory = memory
        else:
            self.memory = None
        if memory_node:
            self.set(memory_node)
        self.initialized = False
        self.familiar = False
        if not strip_query:
            self.reset_node()
        else:
            self.set_id(0)
            self.strip_query = True

    def get_neo4j_legal_labels(self):
        return self.neo4j_legal_labels

    def set_neo4j_legal_labels(self, neo4j_legal_labels):
        self.neo4j_legal_labels = neo4j_legal_labels

    def get_neo4j_legal_relationships(self):
        return self.neo4j_legal_relationships

    def set_neo4j_legal_relationships(self, neo4j_legal_relationships):
        self.neo4j_legal_relationships = neo4j_legal_relationships

    def get_neo4j_legal_properties(self):
        return self.neo4j_legal_properties

    def set_neo4j_legal_properties(self, neo4j_legal_properties):
        self.neo4j_legal_properties = neo4j_legal_properties

    def is_familiar(self):
        if self.initialized is None:
            self.familiar = self.init()
        return self.familiar

    def init(self, memory_node=None):
        result = self.query_for_matching_nodes(memory_node)
        self.initialized = True
        if result is not None:
            self.set(result)
            return True
        else:
            result = self.create(memory_node)
            if result:
                self.set(result)
            else:
                self.initialized = False
        return False

    def query_for_matching_nodes(self, memory_node):
        if isinstance(memory_node, MemoryNodeModel):
            if memory_node.get_label() or memory_node.get_labels():
                nodes = self.memory.get_by_query()
                if nodes and len(nodes) != 0:
                    return nodes[0]
        else:
            raise TypeError("Wrong Type")
        return None

    def create(self, memory_node):
        if isinstance(memory_node, MemoryNodeModel):
            node_id = self.memory.create(memory_node)
            return self.memory.get_by_id(node_id)
        else:
            raise TypeError("Wrong Type")

    def add_information(self, relationship, name):
        if self.memory is not None:
            # First check if node with given name exists by a matching query.
            related_node = MemoryNodeModel(self.memory, MemoryNodeModel(), True)
            related_node.set_properties(neo4j_property.Neo4jProperty().name, name)
            # This adds a label type to the memory query depending on the relation.
            related_node.set_label(neo4j_relationship.Neo4jRelationship.determine_node_type(relationship))
            nodes = self.memory.get_by_query()
            # Pick first from list if multiple matches found.
            if nodes and len(nodes) != 0:
                self.set_relationships(relationship, nodes[0].get_id())
            else:
                node_id = self.memory.create(related_node)
                if node_id != 0:
                    self.set_relationships(relationship, node_id)
            self.memory.save()
            return True
        return False

    def set_strip_query(self, strip):
        self.strip_query = strip

    def is_legal(self):
        # TODO: implement
        pass

    def __str__(self):
        return "NodeModel{" + "memory= " + str(self.memory) + \
               ", id = " + self.id + \
               ", labels = " + self.labels + \
               ", label = " + self.label + \
               ", properties = " + self.properties + \
               ", relationships = " + self.relationships + "}"
