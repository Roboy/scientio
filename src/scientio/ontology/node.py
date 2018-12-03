from __future__ import annotations

import copy
from enum import Enum
from collections import defaultdict
from typing import Union, Set, Dict, List, FrozenSet, Optional

from src.scientio.ontology.json_node import JsonNode
from src.scientio.ontology.otype import OType


class RelationshipAvailability(Enum):
    """
    Show availability of a relationship using this Enum.
    """
    ALL_AVAILABLE = 1
    SOME_AVAILABLE = 2
    NONE_AVAILABLE = 3


class Node(object):
    """
    Get access to all attributes of a Node in the neo4j memory using this class.
    Attributes of Node: ID, Concepts, Relationships, Properties
    """

    NAME_STR: str = "name"
    ID_STR: str = "id"
    id: int
    otype: OType
    entity: str
    meta: FrozenSet[str]
    properties: Dict[str, str]
    relationships: Dict[str, List[int]]

    def __init__(self, node: Node = None, otype: OType = None):
        """
        Construct a new node.

        Args:
            node: create new node from existing node
            concept: give new node a concept like "person" or "robot"
        """
        if node is not None:
            self.set_node(node)
        elif otype is not None:
            self.id = -1
            self.otype = otype
            self.entity = otype.entity
            self.meta = otype.meta
            self.properties = dict().fromkeys(otype.properties, None)
            self.relationships = dict().fromkeys(otype.relationships, [])
        else:
            self.id = -1

    def wipe_id(self):
        """
        Reset the node ID.
        """
        self.id = -1

    def wipe_type(self):
        """
        Reset the node concept.
        """
        self.otype = None

    def wipe_entity(self):
        """
        Reset all node concepts.
        """
        self.entity = ""

    def wipe_meta(self):
        """
        Reset all node concepts.
        """
        self.meta = frozenset()

    def wipe_properties(self):
        """
        Reset all node properties.
        """
        self.properties = dict()

    def wipe_relationships(self):
        """
        Reset all node relationships
        """
        self.relationships = defaultdict(list)

    def wipe_node(self):
        """
        Reset all node attributes.
        """
        self.wipe_id()
        self.wipe_type()
        self.wipe_entity()
        self.wipe_meta()
        self.wipe_properties()
        self.wipe_relationships()

    def get_id(self) -> int:
        """
        Get the node ID.
        """
        return self.id

    def set_id(self, id: int):
        """
        Set the node ID.
        """
        self.id = id

    def get_type(self) -> OType:
        """
        Get the node OType.
        """
        return self.otype

    def set_type(self, otype: OType):
        """
        Get the node OType.
        """
        self.otype = otype

    def get_entity(self) -> str:
        return self.entity

    def get_meta(self) -> FrozenSet:
        """
        Get the set of all node meta.
        """
        return self.meta

    def set_meta(self, meta: FrozenSet):
        """
        Set all the node meta.
        """
        self.meta = meta

    def get_properties(self, key: str=None):
        """Get access to the dictonary of node properties.

        Args:
            key: if a key is given then that specific entry is returned
            otherwise the whole dictonary of properties is returned.
        """
        if key and key in self.properties.keys():
            return self.properties[key]
        return self.properties

    def add_properties(self, values: Dict[str, str]):
        """
        Add properties to the existing properties of a node.

        Args:
            values: one or multiple dictonary entries to add.
        """
        self.properties.update(dict((x, y) for x, y in values.items() if x in self.properties.keys()))

    def set_properties(self, values: Dict[str, str]):
        """
        Add properties to the existing properties of a node.

        Args:
            values: one or multiple dictonary entries to add.
        """
        self.properties = dict((x, y) for x, y in values.items() if x in self.properties.keys())

    def get_relationships(self, key: str=None):
        """
        Get access to the dictonary of node relationships.

        Args:
            key: if a key is given then that specific entry is returned
            otherwise the whole dictonary of relationships is returned.
        """
        if key and key in self.relationships.keys():
            return self.relationships[key]
        return self.relationships

    def add_relationships(self, values: Dict[str, List[int]]):
        """
        Add new relationships to the existing relationships of a node

        Args: ids_per_relationship: one or multiple dictonary entries.
        """
        for key, val in values.items():
            if key in self.relationships.keys():
                self.relationships[key] = list(set(self.relationships.get(key) + val if isinstance(val, list) else [val]))

    def set_relationships(self, values: Dict[str, List[int]]):
        """
        Set a new relationships of a node.

        Args:
            values: one or multiple dictonary entries.
        """
        self.relationships = dict((x, y) for x, y in values.items() if x in self.relationships.keys())

    def has_relationship(self, relationship: str) -> bool:
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
        self.id = copy.deepcopy(node.get_id())
        if node.get_type():
            self.otype = copy.deepcopy(node.get_type())
            self.entity = copy.deepcopy(node.get_entity())
            self.meta = copy.deepcopy(node.get_meta())
            self.properties = copy.deepcopy(node.get_properties())
            self.relationships = copy.deepcopy(node.get_relationships())

    def get_name(self):
        """
        Get the name of the node.
        """
        return self.get_properties(self.NAME_STR)

    def add_name(self, name: str):
        """
        Add the name of the node to the node properties.

        Args:
            name: String with node name.
        """
        self.set_properties(**{self.NAME_STR: name})

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
            if self.has_relationship(predicate):
                at_least_one_available = True
            else:
                all_available = False
        if all_available:
            return RelationshipAvailability.ALL_AVAILABLE
        if at_least_one_available:
            return RelationshipAvailability.SOME_AVAILABLE
        return RelationshipAvailability.NONE_AVAILABLE

    def get_relationships_purity(self, predicates: List[str]) -> Dict[bool, List[str]]:
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
            pure_impure_values.get(self.has_relationship(predicate)).append(predicate)
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

    def to_json(self) -> Optional[JsonNode]:
        """
        TODO
        """
        return None

    def __eq__(self, other: Node):
        """
        Check if two nodes are equal.
        """
        equality = self.get_id() == other.get_id() \
            and self.get_type() == other.get_type() \
            and self.get_entity() == other.get_entity() \
            and self.get_meta() == other.get_meta() \
            and self.get_properties() == other.get_properties() \
            and self.get_relationships() == other.get_relationships()
        return equality

    def __hash__(self):
        """
        Hash node.
        """
        return object.__hash__((self.get_id(), self.get_type(), self.get_entity(), self.get_meta(),
                                self.get_properties(), self.get_relationships()))

    def __str__(self):
        """
        Get string output for node.
        """
        return f'Node(id = {self.id}, ' \
               f'type = {self.otype}, ' \
               f'entity = {self.entity}' \
               f'meta = {self.meta}, ' \
               f'properties = {self.properties}, ' \
               f'relationships = {self.relationships})'

