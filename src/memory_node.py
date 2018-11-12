from src import node
from src import neo4j_label
from src import neo4j_property
from src import neo4j_relationship


class MemoryNodeModel(node.NodeModel):

    def __init__(self, memory, node, strip_query):
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
        if not self.initialized:
            self.familiar = self.init()
        return self.familiar

    def init(self, node):
        result = self.query_for_matching_nodes(node)
        self.initialized = True
        if result:
            self.set(result)
            return True
        else:
            result = self.create(node)
            self.set(result)
        return False

    def query_for_matching_nodes(self, node):
        if self.memory:
            if node.get_label() or node.get_labels():
                nodes = list()
                # try catch
                #TODO get_by_query
                nodes = self.memory.get_by_query

                if __name__ == '__main__':
                    if nodes and not nodes.is_empty():
                        return nodes.get(0)
        return None

    def create(self, node):
        if self.memory:
            pass
        #TODO memory methods

    def add_information(self, relationship, name):
        #TODO
        pass

    def set_strip_query(self, strip):
        self.strip_query = strip

    def __str__(self):
        return "NodeModel{" + "memory= " + self.memory + \
               ", id = " + self.id + \
               ", labels = " + self.labels + \
               ", label = " + self.label + \
               ", properties = " + self.properties + \
               ", relationships = " + self.relationships + "}"