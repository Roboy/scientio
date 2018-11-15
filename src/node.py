from src import neo4j_label
from src import neo4j_property
from src import neo4j_relationship

from enum import Enum

#TODO
# check out better way
class RelationshipAvailability(Enum):
    ALL_AVAILABLE = 1
    SOME_AVAILABLE = 2
    NONE_AVAILABLE = 3


class NodeModel(object):
    def __init__(self, node):
        if node:
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

    def set_id(self, id_):
        self.id = id_

    def get_label(self):
        return self.label

    def get_labels(self):
        return self.labels

    def set_label(self, label: neo4j_label.Neo4jLabel):
        self.label = label
        self.labels.add(label)

    def set_labels(self, label: neo4j_label.Neo4jLabel):
        self.labels.add(label)

    def set_labels(self, labels):
        self.labels.update(labels)

    def get_properties(self):
        return None if len(self.properties) == 0 else self.properties

    def get_properties(self, key: neo4j_property.Neo4jProperty):
        if key:
            return None if len(self.properties) == 0 else self.properties.get(key)
        return None

    def set_properties(self, properties):
        if properties:
            for key in properties.keys():
                self.set_properties(key, properties.get(key))

    def set_properties(self, key: neo4j_property.Neo4jProperty, property_):
        if key:
            new_entry = {key, property_}
            self.properties.update(new_entry)

    def get_relationships(self):
        return None if len(self.relationships) == 0 else self.relationships

    def get_relationships(self, key: neo4j_relationship.Neo4jRelationship):
        if key:
            return None if len(self.relationships) == 0 else self.relationships.get(key)

    def set_relationships(self, relationships):
        if relationships:
            for key in relationships.keys():
                self.set_relationships(key, relationships.get(key))

    def set_relationships(self, key: neo4j_relationship.Neo4jRelationship, ids):
        if key and ids:
            if key in self.relationships:
                self.relationships.get(key).append(ids)
            else:
                new_entry = {key, ids}
                self.relationships.update(new_entry)

    def has_relationships(self, relationship):
        return not (self.get_relationships(relationship) is None) and not self.get_relationships(relationship)

    # def set(self, node: NodeModel):
    def set(self, node):
        self.set_id(node.get_id())
        self.set_relationships(node.get_relationships() if node.get_relationships() is not None else dict())
        self.set_properties(node.get_properties() if node.get_properties() is not None else dict())

    def get_name(self):
        return self.get_properties(neo4j_property.name)

    def add_name(self, name):
        if name:
            self.set_properties(neo4j_property.name, name)

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
        new_entry = {False, new_list}
        pure_impure_values.update(new_entry)
        new_entry = {True, new_list}
        pure_impure_values.update(new_entry)
        for predicate in predicates:
            #TODO
            pure_impure_values.get(self.has_relationships(predicate))
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

    # TODO: does not work
    def __eq__(self, other):
        if self == other:
            return True
        if not isinstance(other, NodeModel):
            return False
        new_node = NodeModel(other)
        equality = self.get_id() == new_node.get_id() and self.get_label() == new_node.get_label() #and \
                   #self.get_labels() == new_node.get_labels() and \
                   #self.get_properties() == new_node.get_properties() and \
                   #self.get_relationships() == new_node.get_relationships()
        # TODO
        return equality

    def __hash__(self):
        return object.__hash__((self.get_id(), self.get_label(), self.get_labels(), self.get_properties(),
                                self.get_relationships()))

    def __str__(self):
        return "NodeModel{" + "id = " + self.id + \
               ", labels = " + self.labels + \
               ", label = " + self.label + \
               ", properties = " + self.properties + \
               ", relationships = " + self.relationships + "}"



