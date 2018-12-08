from typing import FrozenSet, Set, List, Union

import yaml


class OType:
    yaml_tag = u'!OType'

    def __init__(self, *, name, properties=(), relationships=(), meta=()):
        self.name: str = name
        self.properties: FrozenSet[str] = frozenset(properties)
        self.relationships: FrozenSet[str] = frozenset(relationships)
        self.meta: FrozenSet[str] = frozenset(meta)

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"name={self.name}, " \
               f"properties={list(self.properties)}, " \
               f"relationships={list(self.relationships)}, " \
               f"meta={list(self.meta)})"

    def __eq__(self, other: object):
        return isinstance(other, OType) and \
               self.name == other.name and \
               self.properties == other.properties and \
               self.relationships == other.relationships and \
               self.metatypes == other.metatypes

    def __hash__(self):
        return self.name.__hash__()

    @staticmethod
    def _yaml_ctor(loader, node):
        fields = loader.construct_mapping(node, deep=True)
        return OType(**fields)


yaml.add_constructor(OType.yaml_tag, OType._yaml_ctor)
