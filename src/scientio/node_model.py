from scientio.label import Label

from enum import Enum
from collections import defaultdict
from typing import Union, Set, Dict, List


class RelationshipAvailability(Enum):
    ALL_AVAILABLE = 1
    SOME_AVAILABLE = 2
    NONE_AVAILABLE = 3


class NodeModel():

    NAME = "name"
    ID = "id"

    def __init__(self, node=None, strip_query=None):

        # unique nodes ID assigned by memory
        self.id = 0
        # "Person" etc. Duplicate because Memory expects
        # a single Label in CREATE queries, but
        # returns an array of labels inside GET responses.
        self.labels = set()
        self.label = Label()
        # name, birthdate
        self.properties = dict()
        # Relation: <name, list od IDs>
        self.relationships = defaultdict(list)

        self.strip_query = False
        if node is not None:
            self.set_node(node)
        self.strip_query = strip_query

    def reset_id(self):
        self.id = 0

    def reset_label(self):
        self.label = None

    def reset_labels(self):
        self.labels = set()

    def reset_properties(self):
        self.properties = dict()

    def reset_relationships(self):
        self.relationships = defaultdict(list)

    def reset_node(self):
        self.reset_id()
        self.reset_label()
        self.reset_labels()
        self.reset_properties()
        self.reset_relationships()

    def get_id(self):
        return self.id

    def set_id(self, node_id):
        self.id = node_id

    def get_label(self):
        return self.label

    def get_labels(self):
        return self.labels

    # label can be a single Label or a set of multiple Labels
    def set_labels(self, label):
        self.reset_label()
        self.add_labels(label)

    def add_labels(self, label: Union[Label, Set[Label]]):
        if isinstance(label, Label):
            self.label = label
            self.labels |= {label}
        elif isinstance(label, set):
            self.labels |= label

    def get_properties(self, key: str=None):
        if key and key in self.properties:
            return self.properties[key]
        return self.properties

    def set_properties(self, **property_values):
        self.properties.update(property_values)

    def get_relationships(self, key: str=None):
        if key:
            return self.relationships[key]
        return self.relationships

    def set_relationships(self, **ids_per_relationship):
        self.reset_relationships()
        self.add_relationships(**ids_per_relationship)

    def add_relationships(self, **ids_per_relationship):
        for key, value in ids_per_relationship.items():
            if isinstance(value, tuple) or isinstance(value, list):
                self.relationships[key] += value
            else:
                self.relationships[key] += [value]

    def has_relationships(self, relationship: str):
        return len(self.relationships[relationship]) > 0

    def set_node(self, node: NodeModel):
        self.set_id(node.get_id())
        if node.get_label():
            self.set_labels(node.get_label())
            self.add_labels(node.get_labels())
        else:
            self.set_labels(node.get_labels())
        if not node.get_relationships():
            self.reset_relationships()
        else:
            self.set_relationships(**node.get_relationships())
        if not node.get_properties():
            self.reset_properties()
        else:
            self.set_properties(**node.get_properties())

    def get_name(self):
        return self.get_properties(self.NAME)

    def add_name(self, name: str):
        self.set_properties(**{self.NAME : name})

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

    def get_purity_relationships(self, predicates: List[str]) -> Dict[bool, List[str]]:
        pure_impure_values = {False:list(), True:list()}
        for predicate in predicates:
            pure_impure_values.get(self.has_relationships(predicate)).append(predicate)
        return pure_impure_values

    def is_familiar(self):
        # TODO
        pass

    def set_strip_query(self, strip):
        self.strip_query = strip

    def is_legal(self):
        # TODO: implement
        pass

    def __eq__(self, other: NodeModel):
        equality = self.get_id() == other.get_id() \
            and self.get_label() == other.get_label() \
            and self.get_labels() == other.get_labels() \
            and self.get_properties() == other.get_properties() \
            and self.get_relationships() == other.get_relationships()
        return equality

    def __hash__(self):
        return object.__hash__((self.get_id(), self.get_label(), self.get_labels(), self.get_properties(),
                                self.get_relationships()))

    def __str__(self):
        return f'NodeModel{{ id = {self.id}, labels = {self.labels}, label = {self.label}, properties = {self.properties}, relationships = {self.relationships} }}'

