from src.scientio.interfaces.operations import Operations
from src.scientio.ontology import Ontology
from neo4j import GraphDatabase

from scientio.node_model import NodeModel
from typing import Optional


class Neo4j(Operations):
    """
    Implementation of the operations interface for a Neo4j-based graph memory
    """

    _driver: GraphDatabase.driver
    _ontology: Ontology

    def __init__(self, **kwargs):
        try:
            uri = kwargs['neo4j_address']
            user = kwargs['neo4j_username']
            password = kwargs['neo4j_password']
        except KeyError as e:
            raise e
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self._driver.close()

    def create(self, request: NodeModel) -> Optional[NodeModel]:
        if True: # The class of Node is in ontology
            return Neo4j().create_node(request)
        return None

    def retrieve(self, request: NodeModel, node_id: int = None) -> Optional[NodeModel]:
        if node_id is not None and node_id >= 0:
            return self.get_node_by_id(node_id)
        elif node_id is None:
            if True: # The class of Node is in ontology
                return self.get_node(request)
        return None

    def update(self, request: NodeModel) -> Optional[NodeModel]:
        if True: # The class of Node is in ontology
            return self.update_node(request)
        return None

    def delete(self, request: NodeModel) -> bool:
        if request.get_id() >= 0 and self.retrieve(request, request.get_id()) is not None:
            return self.delete_node(request)
        return False

    def _exec_transaction(self, tx, query: str):
        result = tx.run(query)
        return result

    def _exec_query(self, query: str):
        with self._driver.session() as session:
            result = session.write_transaction(self._exec_transaction, query=query).single()[0]
        return result

    def create_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def get_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def get_node_by_id(self, node_id: int) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def update_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def delete_node(self, node: NodeModel) -> bool:
        query = ""  # builder from MNM
        self._exec_query(query)

        if self.get_node_by_id(node.get_id()) is None:
            return True
        else:
            return False