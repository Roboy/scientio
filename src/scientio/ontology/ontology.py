from __future__ import annotations
from typing import FrozenSet, Optional

import copy
import yaml

from src.scientio.ontology.otype import OType


class Ontology(object):
    types: FrozenSet[OType] = None
    entities: FrozenSet[str]
    properties: FrozenSet[str]
    relationships: FrozenSet[str]

    def __init__(self, types_set: FrozenSet[OType] = None, ontology: Ontology = None, path_to_yaml: str = None):
        if types_set is not None:
            self.types = types_set
        elif ontology is not None:
            self.types = copy.deepcopy(ontology.types)
        elif path_to_yaml is not None:
            self.types = self.from_yaml_file(path_to_yaml)

        if self.types is not None:
            self.entities = frozenset([x.entity for x in self.types])
            self.properties = frozenset().union(*[x.properties for x in self.types])
            self.relationships = frozenset().union(*[x.relationships for x in self.types])
        else:
            raise Exception("Empty Ontology is invalid!")

    def from_yaml_file(self, path: str) -> Optional[FrozenSet[OType]]:
        try:
            with open(path, 'r') as f:
                ontology_data = list(yaml.load_all(f))
                return frozenset(ontology_data)
        except yaml.YAMLError as e:
            print("Error in ontology file: ", e)
        return None

    def get_type(self, entity: str) -> Optional[OType]:
        for element in self.types:
            if element.entity == entity:
                return element
        return None

    def __contains__(self, item: OType):
        return item in self.types
