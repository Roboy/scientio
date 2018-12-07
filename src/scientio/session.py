from typing import Type, List

from src.scientio.drivers.neo4j_driver import Neo4jDriver
from src.scientio.interfaces.operations import Operations
from src.scientio.ontology.node import Node
from src.scientio.ontology.ontology import Ontology


class Session(Operations):
    """
    Lightweight wrapper around a scientio ontology session,
     powered by a certain named operations drivers.
    """

    """
    Use Neo4jDriver as a possible value for `driver_name` in the Session constructor.
    """
    Neo4jDriver = "neo4j"

    """
    The operations driver which is used by this session.
    """
    _driver: Operations

    def __init__(self, *, driver_name: str=Neo4jDriver, ontology: Ontology, **kwargs):
        """
        Instantiate a session with a certain ontology, a certain driver, and certain additional
         key-word arguments which may be necessary to instantiate the driver.
        :param driver_name: Name of the driver. Currently, only the value `Session.Neo4jDriver` is allowed.
        :param ontology: The Scientio Ontology by which Nodes in this Session are allowed to be created,
         retrieved and updated.
        :param kwargs: Driver-specific key-word arguments which are necessary to instantiate
         the selected Operations driver. The following key-word arguments are required per driver:

         +------------------+----------------------------------------------------------+
         | Driver name      | Arguments required                                       |
         +------------------+----------------------------------------------------------+
         | Neo4jDriver      | neo4j_address:  URI for the Neo4j database.              |
         |                  | neo4j_username: Username for the Neo4j database.         |
         |                  | neo4j_password: Password for the Neo4j database.         |
         +------------------+----------------------------------------------------------+
        """
        self._driver = Session._driver_for_name(driver_name)(ontology=ontology, **kwargs)

    def create(self, request: Node) -> Node:
        """
        Create a new Node by a certain Node specification.
        Note: The node will only be persisted, if it is legal wrt/ it's properties/relationships,
         given it's Concept from this Session's ontology.
        :param request: The node to persist. Note, that the
         `request` Node must have a set Concept from this Session's ontology,
         and no ID assigned (yet).
        :return: The created Node if successful, None otherwise.
        """
        return self._driver.create(request)

    def retrieve(self, request: Node = None, node_id: int = None) -> List[Node]:
        """
        Retrieve a node, by match or by id.
        :param request: Set to a certain Node specification for retrieval-
         by-match. The node may have certain set property values and/or relationships,
         which retrieved nodes are required to match.
        :param node_id: A node id for retrieval-by-id. Set this to any integer
         to retrieve the Node with the specified integer id.
        :return: A Node which matches the criteria, None if no such Node exists.
        """
        return self._driver.retrieve(request)

    def update(self, request: Node) -> Node:
        """
        Persist changes to node properties/concept/relationships made on a Node
         which was previosuly obtained through `retrieve()` or `create()`.
        Note: The node will only be persisted, if it is legal wrt/ it's properties/relationships,
         given it's Concept from this Session's ontology.
        :param request: The node whose changed properties/concept/relationships should be persisted.
        :return: The persisted node, or None if the Operation failed.
        """
        return self._driver.update(request)

    def delete(self, request: Node) -> bool:
        """
        Delete a node which was previously obtained through `retrieve()` or `create()`.
        :param request: The node to delete.
        :return: True if the node was deleted successfully, False otherwise.
        """
        return self._driver.delete(request)

    @staticmethod
    def _driver_for_name(driver_name: str) -> Type:
        return {
            Session.Neo4jDriver: Neo4jDriver
        }[driver_name]
