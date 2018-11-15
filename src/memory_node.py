from src import node
from src import memory_interface
from src import neo4j_relationship
from src import neo4j_property


class MemoryNodeModel(node.NodeModel):

    def __init__(self, memory: memory_interface.MemoryInterface, node: node.NodeModel, strip_query):
        # GSON stuff: @Expose: private transient boolean stripQuery
        self.strip_query = False
        # supposed to be Neo4jMemoryInterface
        self.memory = None
        if memory:
            self.memory = memory
        if node:
            self.set(node)
        self.initialized = False
        self.familiar = False
        super(MemoryNodeModel, self).__init__()
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

    def init(self, node):
        result = self.query_for_matching_nodes(node)
        self.initialized = True
        if result is not None:
            self.set(result)
            return True
        else:
            result = self.create(node)
            if result:
                self.set(result)
            else:
                self.initialized = False
        return False

    def query_for_matching_nodes(self, node):
        if self.memory is not None:
            if node.get_label() or node.get_labels():
                nodes = self.memory.get_by_query()
                if nodes and len(nodes) != 0:
                    return nodes[0]
        return None

    def create(self, node):
        if self.memory is not None:
            id_ = self.memory.create(node)
            return self.memory.get_by_id(id_)

    def add_information(self, relationship, name):
        if self.memory is not None:
            # First check if node with given name exists by a matching query.
            related_node = MemoryNodeModel(True, self.memory)
            related_node.set_properties(neo4j_property.Neo4jProperty.name, name)
            # This adds a label type to the memory query depending on the relation.
            related_node.set_label(neo4j_relationship.Neo4jRelationship.determine_node_type(relationship))
            nodes = self.memory.get_by_query()
            # Pick first from list if multiple matches found.
            if nodes and len(nodes) != 0:
                self.set_relationships(relationship, nodes[0].get_id())
            else:
                id_ = self.memory.create(related_node)
                if id_ != 0:
                    self.set_relationships(relationship, id_)
            self.memory.save()
            return True
        return False

    def set_strip_query(self, strip):
        self.strip_query = strip

    def is_legal(self):
        # TODO: implement
        return True

    def __str__(self):
        return "NodeModel{" + "memory= " + self.memory + \
               ", id = " + self.id + \
               ", labels = " + self.labels + \
               ", label = " + self.label + \
               ", properties = " + self.properties + \
               ", relationships = " + self.relationships + "}"

