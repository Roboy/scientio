from typing import Optional

from neo4j import GraphDatabase

from src.scientio.interfaces.operations import Operations
from src.scientio.ontology.node import Node
from src.scientio.ontology.ontology import Ontology


class Neo4j(Operations):
    """
    Implementation of the operations interface for a Neo4j-based graph memory
    """

    _driver: GraphDatabase.driver
    _ontology: Ontology

    def __init__(self, *, ontology, **kwargs):
        try:
            uri = kwargs['neo4j_address']
            user = kwargs['neo4j_username']
            password = kwargs['neo4j_password']
        except KeyError as e:
            raise e
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self._driver.close()

    def create(self, request: Node) -> Optional[Node]:
        if True: # The class of Node is in ontology
            return self.create_node(request)
        return None

    def retrieve(self, request: Node, node_id: int = None) -> Optional[Node]:
        if node_id is not None and node_id >= 0:
            return self.get_node_by_id(node_id)
        elif node_id is None:
            if True: # The class of Node is in ontology
                return self.get_node(request)
        return None

    def update(self, request: Node) -> Optional[Node]:
        if True: # The class of Node is in ontology
            return self.update_node(request)
        return None

    def delete(self, request: Node) -> bool:
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

    def create_node(self, node: Node) -> Optional[Node]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def get_node(self, node: Node) -> Optional[Node]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def update_node(self, node: Node) -> Optional[Node]:
        query = ""  # builder from MNM
        result = self._exec_query(query)
        result_node = None  # node from result
        return result_node

    def delete_node(self, node: Node) -> bool:
        query = ""  # builder from MNM
        self._exec_query(query)

        if self.get_node_by_id(node.get_id()) is None:
            return True
        else:
            return False