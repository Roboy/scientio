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
        #chech if labels == null
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
            self.properties.update(key, property_)

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
            # here i am its not a todo