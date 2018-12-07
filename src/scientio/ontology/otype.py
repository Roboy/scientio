from typing import FrozenSet

import yaml


class OType(yaml.YAMLObject):
    yaml_tag = u'!OType'

    def __init__(self, entity, properties, relationships, meta):
        self.entity: str = entity
        self.properties: FrozenSet[str] = frozenset(properties)
        self.relationships: FrozenSet[str] = frozenset(relationships)
        self.meta: FrozenSet[str] = frozenset(meta)

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"type={self.entity}, " \
               f"properties={list(self.properties)}, " \
               f"relationships={list(self.relationships)}, " \
               f"meta={list(self.meta)})"

    def __eq__(self, other: object):
        return isinstance(other, OType) and \
            self.entity == other.entity and \
            self.properties == other.properties and \
            self.relationships == other.relationships and \
            self.meta == other.meta

    def __hash__(self):
        return object.__hash__((self.entity, self.properties, self.relationships, self.meta))
