from src import neo4j_label
from src import neo4j_property
from src import neo4j_relationship
from enum import Enum


class RelationshipAvailability(Enum):
    ALL_AVAILABLE = 1
    SOME_AVAILABLE = 2
    NONE_AVAILABLE = 3


class NodeModel(object):
    def __init__(self, node):
        if node is not None:
            self.set(node)
        # unique nodes ID assigned by memory
        self.id = 0
        # "Person" etc. Duplicate because Memory expects a single Label in CREATE queries, but
        # returns an array of labels inside GET responses.
        self.labels = set()
        self.label = None
        # name, birthdate
        self.properties = dict()
        # Relation: <name, list od IDs>
        self.relationships = dict()
        self.neo4j_legal_labels = set()
        self.neo4j_legal_properties = set()
        self.neo4j_legal_relationships = set()

    def get_id(self):
        return self.id

    def set_id(self, node_id):
        self.id = node_id

    def get_label(self):
        return self.label

    def get_labels(self):
        return self.labels

    def set_label(self, label):
        if isinstance(label, neo4j_label.Neo4jLabel):
            self.label = label
            self.labels.add(label)
        if isinstance(label, set):
            for i in label:
                self.labels.add(i)
        else:
            raise TypeError("Wrong Type")

    def set_labels(self, labels: set):
        for label in labels:
            self.labels.add(label)

    def get_properties(self, key: neo4j_property.Neo4jProperty = None):
        if len(self.properties) > 0:
            if key is not None:
                return self.properties.get(key)
            return self.properties
        return None

    def set_properties(self, properties, key):
        if isinstance(properties, neo4j_property.Neo4jProperty):
            if key is not None:
                self.properties[key] = properties
        elif isinstance(properties, dict):
            for k in properties.keys():
                self.set_properties(properties.get(k), k)
        else:
            raise TypeError("Wrong Type")

    def get_relationships(self, key: neo4j_relationship.Neo4jRelationship = None):
        if len(self.relationships) > 0:
            if key is not None:
                return self.relationships.get(key)
            return self.relationships
        return None

    def set_relationships(self, key, ids = None):
        if isinstance(key, neo4j_relationship.Neo4jRelationship):
            if key in self.relationships:
                self.relationships.get(key).append(ids)
            else:
                self.relationships[key] = ids
        elif isinstance(key, dict):
            for k in key.keys():
                self.set_relationships(k, key.get(k))
        else:
            raise TypeError("Wrong Type")

    def has_relationships(self, relationship):
        if self.get_relationships(relationship) is not None:
            if len(self.get_relationships(relationship)) != 0:
                return True
        return False

    def set(self, node):
        if isinstance(node, NodeModel):
            self.set_id(node.get_id())
            if node.get_relationships() is None:
                self.set_relationships(dict())
            else:
                self.set_relationships(node.get_relationships())
            if node.get_properties() is None:
                self.set_relationships(dict())
            else:
                self.set_relationships(node.get_properties())
        else:
            raise TypeError("Wrong Type")

    def get_name(self):
        return self.get_properties(neo4j_property.Neo4jProperty().name)

    def add_name(self, name):
        if name is not None:
            self.set_properties(neo4j_property.Neo4jProperty().name, name)

    def check_relationship_availability(self, relationships):
        all_available = True
        at_least_one_available = False
        for predicate in relationships:
            if self.has_relationships(predicate):
                at_least_one_available = True
            else:
                all_available = False
        if all_available:
            return RelationshipAvailability.ALL_AVAILABLE
        if at_least_one_available:
            return RelationshipAvailability.SOME_AVAILABLE
        return RelationshipAvailability.NONE_AVAILABLE

    def get_purity_relationships(self, predicates):
        pure_impure_values = dict()
        new_list = list()
        pure_impure_values[False] = new_list
        pure_impure_values[True] = new_list
        for predicate in predicates:
            pure_impure_values.get(self.has_relationships(predicate)).append(predicate)
        return pure_impure_values

    # def isLegal()

    def reset_id(self):
        self.id = 0

    def reset_label(self):
        self.label = None

    def reset_labels(self):
        self.labels = set()

    def reset_properties(self):
        self.properties = dict()

    def reset_relationships(self):
        self.relationships = dict()

    def reset_node(self):
        self.reset_id()
        self.reset_label()
        self.reset_labels()
        self.reset_properties()
        self.reset_relationships()

    def __eq__(self, other):
        if self == other:
            return True
        if not isinstance(other, NodeModel):
            return False
        new_node = NodeModel(other)
        equality = self.get_id() == new_node.get_id() \
            and self.get_label() == new_node.get_label() \
            and self.get_labels() == new_node.get_labels() \
            and self.get_properties() == new_node.get_properties() \
            and self.get_relationships() == new_node.get_relationships()
        return equality

    def __hash__(self):
        return object.__hash__((self.get_id(), self.get_label(), self.get_labels(), self.get_properties(),
                                self.get_relationships()))

    def __str__(self):
        return "NodeModel{" + "id = " + str(self.id) + \
               ", labels = " + str(self.labels) + \
               ", label = " + self.label + \
               ", properties = " + str(self.properties) + \
               ", relationships = " + str(self.relationships) + "}"
