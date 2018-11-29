from scientio.label import Label

from enum import Enum
from collections import defaultdict
from typing import Union, Set, Dict, List


class RelationshipAvailability(Enum):
    """
    Show availability of a relationship using this Enum.
    """
    ALL_AVAILABLE = 1
    SOME_AVAILABLE = 2
    NONE_AVAILABLE = 3


class NodeModel():
    """
    Get access to all attributes of a NodeModel in the neo4j memory using this class.
    Attributes of NodeModel: ID, Labels, Relationships, Properties 
    """

    NAME = "name"
    ID = "id"

    def __init__(self, node=None, label=None):
        """
        Construct a new node.

        Args:
            node: create new node from existing node
            label: give new node a main label like "person" or "robot"
        """
        self.id = 0
        self.labels = set()
        self.label = label
        self.properties = dict()
        self.relationships = defaultdict(list)
        self.strip_query = None
        if node is not None:
            self.set_node(node)

    def reset_id(self):
        """
        Reset the node ID.
        """
        self.id = 0

    def reset_label(self):
        """
        Reset the node main label.
        """
        self.label = None

    def reset_labels(self):
        """
        Reset all node labels.
        """
        self.labels = set()

    def reset_properties(self):
        """
        Reset all node properties.
        """
        self.properties = dict()

    def reset_relationships(self):
        """
        Reset all node relationships
        """
        self.relationships = defaultdict(list)

    def reset_node(self):
        """
        Reset all node attributes.
        """
        self.reset_id()
        self.reset_label()
        self.reset_labels()
        self.reset_properties()
        self.reset_relationships()

    def get_id(self):
        """
        Get the node ID.
        """
        return self.id

    def set_id(self, node_id):
        """
        Set the node ID.
        """
        self.id = node_id

    def get_label(self):
        """
        Get the node main label.
        """
        return self.label

    def get_labels(self):
        """
        Get the set of all node labels.
        """
        return self.labels

    # label can be a single Label or a set of multiple Labels
    def set_labels(self, label):
        """Set all the node labels."""
        self.reset_label()
        self.add_labels(label)

    def add_labels(self, label: Union[Label, Set[Label]]):
        """Add new labels to the existing labels of the node.

        Args: 
            label: is either a string or a set of strings.
        """
        if isinstance(label, Label):
            self.label = label
            self.labels |= {label}
        elif isinstance(label, set):
            self.labels |= label

    def get_properties(self, key: str=None):
        """Get access to the dictonary of node properties. 
        
        Args:
            key: if a key is given then that specific entry is returned
            otherwise the whole dictonary of properties is returned.
        """
        if key and key in self.properties:
            return self.properties[key]
        return self.properties

    def set_properties(self, **property_values):
        """
        Add properties to the existing properties of a node. 

        Args:
            property_values: one or multiple dictonary entries to add.
        """
        self.properties.update(property_values)

    def get_relationships(self, key: str=None):
        """
        Get access to the dictonary of node relationships.

        Args:
            key: if a key is given then that specific entry is returned
            otherwise the whole dictonary of relationships is returned.
        """
        if key:
            return self.relationships[key]
        return self.relationships

    def set_relationships(self, **ids_per_relationship):
        """
        Set a new relationships of a node. 

        Args: 
            ids_per_relationship: one or multiple dictonary entries.
        """
        self.reset_relationships()
        self.add_relationships(**ids_per_relationship)

    def add_relationships(self, **ids_per_relationship):
        """
        Add new relationships to the existing relationships of a node

        Args: ids_per_relationship: one or multiple dictonary entries.
        """
        for key, value in ids_per_relationship.items():
            if isinstance(value, tuple) or isinstance(value, list):
                self.relationships[key] += value
            else:
                self.relationships[key] += [value]

    def has_relationships(self, relationship: str):
        """
        Check if node has a specific relationship.

        Args:
            relationship: String that represents an existing relationship type.
        """
        return len(self.relationships[relationship]) > 0

    def set_node(self, node: NodeModel):
        """
        Get a node given an existing node. 

        Args:
            node: another NodeModel object.
        """
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
        """
        Get the name of the node.
        """
        return self.get_properties(self.NAME)

    def add_name(self, name: str):
        """
        Add the name of the node to the node properties.

        Args:
            name: String with node name.
        """
        self.set_properties(**{self.NAME : name})

    def check_relationship_availability(self, relationships):
        """
        Check the availability of certain relationships of a node. 

        Args:
            relationships: list of relationships.

        Returns:
            One member of the RelationshipAvailability Enum: ALL_AVAILABLE, SOME_AVAILABLE, NONE_AVAILABLE 
        """
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
        """
        Compare the relationships the node has with a list of relationships. 

        Args:
            predicates: List of strings representing diffrent relationships.

        Returns:
            A dictonary: the key "True" holds a list of relationships that the node has 
            and the key "False" all relationships the node does not haves
        """
        pure_impure_values = {False:list(), True:list()}
        for predicate in predicates:
            pure_impure_values.get(self.has_relationships(predicate)).append(predicate)
        return pure_impure_values

    def is_familiar(self):
        """
        TODO
        """
        pass

    def is_legal(self):
        """
        TODO
        """
        pass

    def __eq__(self, other: NodeModel):
        """
        Check if two nodes are equal.
        """
        equality = self.get_id() == other.get_id() \
            and self.get_label() == other.get_label() \
            and self.get_labels() == other.get_labels() \
            and self.get_properties() == other.get_properties() \
            and self.get_relationships() == other.get_relationships()
        return equality

    def __hash__(self):
        """
        Hash node.
        """
        return object.__hash__((self.get_id(), self.get_label(), self.get_labels(), self.get_properties(),
                                self.get_relationships()))

    def __str__(self):
        """
        Get string output for node.
        """
        return f'NodeModel{{ id = {self.id}, labels = {self.labels}, label = {self.label}, properties = {self.properties}, relationships = {self.relationships} }}'

