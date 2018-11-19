from src import memory_node_model


# I'm a stub
class MemoryInterface(object):

    def __init__(self):
        pass

    def get_by_query(self):
        nodes = list()
        node = memory_node_model.MemoryNodeModel()
        nodes.append(node)
        return nodes

    def create(self, node):
        pass

    def get_by_id(self, id_):
        pass

    def save(self):
        pass

    def __str__(self):
        return "Memory"
