import copy
from enum import Enum
from collections import defaultdict
from typing import Dict, List, FrozenSet, Optional, Union, Any, Set

from ..ontology.json_node import JsonNode
from ..ontology.otype import OType


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
    Attributes of Node: ID, Type, Relationships, Properties
    """

    NAME_STR: str = "name"
    ID_STR: str = "id"

    id: int
    otype: OType
    entity: str
    meta: FrozenSet[str]
    properties: Dict[str, str]
    relationships: Dict[str, Set[int]]

    def __init__(self, node: 'Node' = None, metatype: OType = None):
        """
        Construct a new node.
        :param node: create new node from existing node
        :param metatype: give new node a meta like "person" or "robot"
        """
        self.id = -1
        if node is not None:
            self.set_node(node)
        elif metatype is not None:
            self.set_type(metatype)

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
        Reset all node meta.
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
        self.meta = otype.meta
        self.entity = otype.entity
        self.properties = dict().fromkeys(otype.properties, "")
        self.relationships = {rel: set() for rel in otype.relationships}

    def set_entity(self, entity: str):
        self.entity = entity

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

    def get_properties(self, key: str=None) -> Union[Any, Dict[str, Any]]:
        """
        Get access to the dictonary of node properties.
        :param key: Specific property name whose value should be returned.
        :return: If a key is given and it exists, the corresponding value is returned.
         Otherwise the whole dictonary of properties is returned.
        """
        if key and key in self.properties:
            return self.properties[key]
        return self.properties

    def set_properties(self, values: Dict[str, Any]) -> None:
        """
        Add properties to the existing properties of a node.
        :param values: One or multiple dictonary entries to add.
        """
        self.properties.update({key: value for key, value in values.items() if key in self.properties})

    def get_relationships(self, key: str=None) -> Union[Set[int], Dict[str, Set[int]]]:
        """
        Get access to the dictonary of node relationships.
        :param key: Specify the name of a relationship to retrieve
         the node ids for a particular relationship.
        :return: If a key is given then that specific entry is returned,
         otherwise the whole dictionary of relationships is returned.
        """
        if key and key in self.relationships:
            return self.relationships[key]
        return self.relationships

    def add_relationships(self, values: Dict[str, Set[int]]) -> None:
        """
        Add new relationships to the existing relationships of a node
        :param values: Dictionary from relationship names to
          key sets, which should be merged with the existing entries
          for the respective relationship.
        """
        for key, val in values.items():
            if key in self.relationships:
                self.relationships[key] |= val if isinstance(val, set) else {val}

    def set_relationships(self, values: Dict[str, Set[int]]):
        """
        Replace relationships of of a node.
        :param values: Dictionary from relationship names to
          key sets, which should replace the existing entries
          for the respective relationship.
        """
        for key, val in values.items():
            if key in self.relationships:
                self.relationships[key] = val if isinstance(val, set) else {val}

    def has_relationship(self, relationship: str) -> bool:
        """
        Check if node has a specific relationship.
        :param relationship: The name of the relationship to be checked.
        :return: True if the relationship is allowed, false otherwise.
        """
        return relationship in self.relationships and len(self.relationships[relationship]) > 0

    def set_node(self, node: 'Node') -> None:
        """
        Copy all attributes of another node.
        Hint: The other node's metatype will only be copied, if it
         is notnull. Otherwise, this node will keep it's metatype.
        :param node: The node object to copy.
        """
        self.id = node.get_id()
        self.properties = copy.deepcopy(node.get_properties())
        self.relationships = copy.deepcopy(node.get_relationships())
        if node.get_type():
            self.otype = node.get_type()
            self.meta = copy.deepcopy(node.get_meta())
            self.entity = copy.deepcopy(node.get_entity())

    def get_name(self) -> str:
        """
        Get the name of the node.
        """
        return self.get_properties(self.NAME_STR)

    def set_name(self, name: str) -> None:
        """
        Add the name of the node to the node properties.
        :param name: New name for the node.
        """
        self.set_properties({self.NAME_STR: name})

    def check_relationship_availability(self, relationships: List[str]) -> RelationshipAvailability:
        """
        Check the availability of certain relationships of a node.
        :param relationships: list of relationships.
        :return: ALL_AVAILABLE if all listed relationships are available,
         SOME_AVAILABLE if some of the listed relationships are available,
         NONE_AVAILABLE otherwise.
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
        :param predicates: List of strings representing different relationships.
        :return: A dictionary: the key "True" holds a list of relationships that the node has,
         and the key "False" all relationships the node does not have.
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

    def __eq__(self, other: 'Node'):
        """
        Check if two nodes are equal.
        """
        equality = self.get_id() == other.get_id() \
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
               f'entity = {self.entity}, ' \
               f'meta = {self.meta}, ' \
               f'properties = {self.properties}, ' \
               f'relationships = {self.relationships})'

