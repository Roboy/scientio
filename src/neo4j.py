from typing import Optional

from neo4j import GraphDatabase

from src.node_model import NodeModel


class Neo4j(object):
    _driver: GraphDatabase.driver = None

    def __init__(self, **kwargs):
        if kwargs is not None:
            if kwargs['neo4j_address']:
                uri = kwargs['neo4j_address']
            else:
                raise KeyError
            if kwargs['neo4j_username']:
                user = kwargs['neo4j_username']
            else:
                raise KeyError
            if kwargs['neo4j_password']:
                password = kwargs['neo4j_password']
            else:
                raise KeyError
        else:
            raise ValueError

        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    @staticmethod
    def _create_and_return_query(tx, query: str):
        result = tx.run(query)
        return result.single()[0]

    def create_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = "" # builder from MNM
        with self._driver.session() as session:
            result = session.write_transaction(self._create_and_return_query, query=query)
        result_node = None # node from result
        return result_node

    def get_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        with self._driver.session() as session:
            result = session.write_transaction(self._create_and_return_query, query=query)
        result_node = None  # node from result
        return result_node

    def get_node_by_id(self, node_id: int) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        with self._driver.session() as session:
            result = session.write_transaction(self._create_and_return_query, query=query)
        result_node = None  # node from result
        return result_node

    def update_node(self, node: NodeModel) -> Optional[NodeModel]:
        query = ""  # builder from MNM
        with self._driver.session() as session:
            result = session.write_transaction(self._create_and_return_query, query=query)
        result_node = None  # node from result
        return result_node

    def delete_node(self, node: NodeModel) -> bool:
        query = ""  # builder from MNM
        with self._driver.session() as session:
            result = session.write_transaction(self._create_and_return_query, query=query)

        if self.get_node_by_id(node.get_id()) is None:
            return True
        else:
            return False
