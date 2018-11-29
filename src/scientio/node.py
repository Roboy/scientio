from scientio.concept import Concept

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


class Node():
    """
    Get access to all attributes of a Node in the neo4j memory using this class.
    Attributes of Node: ID, Concepts, Relationships, Properties 
    """

    NAME = "name"
    ID = "id"

    def __init__(self, node=None, concept=None):
        """
        Construct a new node.

        Args:
            node: create new node from existing node
            concept: give new node a concept like "person" or "robot"
        """
        self.id = 0
        self.concept = concept
        self.concepts = set()
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

    def reset_concept(self):
        """
        Reset the node concept.
        """
        self.concept = None

    def reset_concepts(self):
        """
        Reset all node concepts.
        """
        self.concepts = set()

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
        self.reset_concept()
        self.reset_concepts()
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

    def get_concept(self):
        """
        Get the node concept.
        """
        return self.concept

    def get_concepts(self):
        """
        Get the set of all node concepts.
        """
        return self.concepts

    def set_concepts(self, concept):
        """Set all the node concepts."""
        self.reset_concept()
        self.add_concepts(concept)

    def add_concepts(self, concept: Union[Concept, Set[Concept]]):
        """Add new concepts to the existing concepts of the node and set the concept.

        Args: 
            concept: is either a string or a set of strings.
        """
        if isinstance(concept, Concept):
            self.concept = concept
            self.concepts |= {concept}
        elif isinstance(concept, set):
            self.concepts |= concept

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

    def set_node(self, node: Node):
        """
        Get a node given an existing node. 

        Args:
            node: another Node object.
        """
        self.set_id(node.get_id())
        if node.get_concept():
            self.set_concepts(node.get_concept())
            self.add_concepts(node.get_concepts())
        else:
            self.set_concepts(node.get_concepts())
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

    def __eq__(self, other: Node):
        """
        Check if two nodes are equal.
        """
        equality = self.get_id() == other.get_id() \
            and self.get_concept() == other.get_concept() \
            and self.get_concepts() == other.get_concepts() \
            and self.get_properties() == other.get_properties() \
            and self.get_relationships() == other.get_relationships()
        return equality

    def __hash__(self):
        """
        Hash node.
        """
        return object.__hash__((self.get_id(), self.get_concept(), self.get_concepts(), self.get_properties(),
                                self.get_relationships()))

    def __str__(self):
        """
        Get string output for node.
        """
        return f'Node{{ id = {self.id}, concepts = {self.concepts}, concept = {self.concept}, properties = {self.properties}, relationships = {self.relationships} }}'

