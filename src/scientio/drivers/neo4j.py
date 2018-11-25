# I'm a stub for the neo4j connection

# Probably Neo4j methods can be all static ...
from src.scientio.operations import Operations
from src.scientio.ontology import Ontology
from neo4j import GraphDatabase

from src.scientio.memory_node_model import MemoryNodeModel
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

    def create(self, request: MemoryNodeModel) -> Optional[MemoryNodeModel]:
        return None

    def retrieve(self, request: MemoryNodeModel, node_id: int = None) -> Optional[MemoryNodeModel]:
        return None

    def update(self, request: MemoryNodeModel) -> Optional[MemoryNodeModel]:
        return None

    def delete(self, request: MemoryNodeModel) -> bool:
        return False

    def _exec_query(self, query: str):
        with self._driver.session() as session:
            result = session.write_transaction(query=query)
        return result
