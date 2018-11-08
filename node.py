class NodeModel(object):
    def __init__(self):
        # unique nodes ID assigned by memory
        self.id = 0
        # "Person" etc. Duplicate because Memory expects a single Label in CREATE queries, but
        # returns an array of labels inside GET responses.
        self.labels = set()
        self.label = 0
        # name, birthdate
        self.properties = dict()
        # Relation: <name as String, ArrayList of IDs (constraints related to this node over this relation)>
        self.relationships = dict()

    def get_id(self):
        return self.id

    def set_id(self, id_):
        self.id = id_

    def get_label(self):
        return self.labels

    def set_label(self, label):
        if self.labels is None:
            self.labels = set()
        self.label = label
        self.labels.add(label)

    def set_labels(self, label):
        if self.labels is None:
            self.labels = set()
        if self.labels is not None:
            self.labels.add(label)

    def set_labels(self, labels):
        if self.labels is None:
            self.labels = set()
        if self.labels is not None:
            self.labels.update(labels)

    def get_properties(self):
        return None if (self.properties is None or len(self.properties) == 0) else self.properties

    def get_property(self, key):
        if key is not None:
            return None if (self.properties is None or len(self.properties) == 0) else self.properties.get(key)

    def set_properties(self, properties):
        if self.properties is None:
            self.properties = dict()
        if properties is not  None:
            for key in properties.keys():
                self.set_property(key, properties.get(key))

    def set_property(self, key, property_):
        if self.properties is None:
            self.properties = dict()
        if key is not None and property is not None:
            new_entry = {key, property_}
            self.properties.update(new_entry)

    def get_relationships(self):
        return None if (self.relationships is None or len(self.relationships) == 0) else self.relationships

    def get_relationship(self, key):
        if key is not None:
            return None if (self.relationships is None or len(self.relationships) == 0) else self.relationships.get(key)

    def set_relationships(self, relationships):
        if self.relationships is None:
            self.relationships = dict()
        if relationships is not None:
            for key in relationships.keys():
                self.set_relationship(key, relationships.get(key))

    def set_relationship(self, key, ids):
        if self.relationships is None:
            self.relationships = dict()

        if key is not None and ids is not None:
            if key in self.relationships:
                self.relationships.get(key).append(ids)
            else:
                new_entry = {key, ids}
                self.relationships.update(new_entry)

    def has_relationship(self, relationship):
        return not (self.get_relationship(relationship) is None) and not self.get_relationship(relationship)

    # TODO defne the neo4j properties
    # def set(self, node: NodeModel):
    #    if node is not None:
    #        self.set_id(node.get_id())
    #        self.set_relationships()

    # def get_name(self):

    # def add_name():

    # def checkRelationshipAvailability()

    # def getPurityRelationships()

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

    # @ Override : equals(Object obj)
    # @ Override : hashCode()
    # @ Override : toString()