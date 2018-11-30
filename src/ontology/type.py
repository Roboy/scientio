import yaml


class Type(yaml.YAMLObject):
    yaml_tag = u'!Type'
    def __init__(self, type, properties, relationships, meta=None):
        self.type: frozenset = frozenset(type)
        self.properties: frozenset = frozenset(properties)
        self.relationships: frozenset = frozenset(relationships)
        self.meta: frozenset = frozenset(meta) if meta is not None else None

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"type={list(self.type)}, " \
               f"properties={list(self.properties)}, " \
               f"relationships={list(self.relationships)}, " \
               f"meta={list(self.meta)})"
