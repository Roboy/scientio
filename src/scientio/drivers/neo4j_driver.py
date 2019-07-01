from typing import Optional, Dict, List, Set

from neo4j import GraphDatabase
from neo4j import Node as Neo4jNode

from ..interfaces.operations import Operations
from ..ontology.node import Node
from ..ontology.ontology import Ontology
from ..ontology.otype import OType
from ..util.query_builder import QueryBuilder


class Neo4jDriver(Operations):
    """
    Implementation of the operations interface for a Neo4j-based graph memory
    TODO: Refactor the naked Cypher expressions to QueryBuilder
    """

    _driver: GraphDatabase.driver
    _ontology: Ontology

    def __init__(self, ontology, **kwargs):
        try:
            uri = kwargs['neo4j_address']
            user = kwargs['neo4j_username']
            password = kwargs['neo4j_password']
        except KeyError as e:
            raise e
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._ontology = ontology

    def __del__(self):
        self._driver.close()

    def create(self, request: Node) -> Optional[Node]:
        if self._ontology.__contains__(request.get_type()):  # The class of Node is in ontology
            return self.create_node(request)
        print(f"No such type in ontology: the {request.get_type()} is missing")  # Error
        return None

    def retrieve(self, request: Node = None, node_id: int = None) -> Optional[List[Node]]:
        if node_id is not None and node_id >= 0:
            return self.get_node_by_id(node_id)
        else:
            if request is not None and self._ontology.__contains__(request.get_type()):  # The class of Node is in ontology
                return self.get_node(request)
        print(f"No such type in ontology: the {request.get_type()} is missing")  # Error
        return None

    def update(self, request: Node) -> Optional[Node]:
        if self._ontology.__contains__(request.get_type()) and request.get_id() >= 0:  # The class of Node is in ontology
            return self.update_node(request)
        print(f"No such type in ontology: the {request.get_type()} is missing")  # Error
        return None

    def delete(self, request: Node) -> bool:
        if request.get_id() >= 0:
            return self.delete_properties_relationships(request)
        return False

    def _exec_transaction(self, tx, query: str):
        result = tx.run(query)
        return result

    def _exec_query(self, query: str, single=True):
        with self._driver.session() as session:
            if single:
                result = session.write_transaction(self._exec_transaction, query=query).single()
            else:
                bolt_statement = session.write_transaction(self._exec_transaction, query=query)
                result = []
                for record in bolt_statement:
                    result.append(record)
        return result

    def create_node(self, req: Node) -> Optional[Node]:
        builder = QueryBuilder()
        builder.add("CREATE (a:" + req.get_entity())
        if req.get_meta() is not None and len(req.get_meta()) > 0:
            builder.add_meta(req.get_meta())
        builder.add_parameters(req.get_properties()).add(") RETURN a")

        record: Neo4jNode = self._exec_query(builder.get())[0]
        req.set_id(int(record.id))
        return req

    def get_node(self, req: Node) -> Optional[List[Node]]:
        builder = QueryBuilder()
        if req.get_entity() is not None:
            builder.add(f"MATCH (n:{req.get_entity()}")
            if req.get_meta() is not None and len(req.get_meta()) > 0:
                builder.add_meta(req.get_meta())
        else:
            builder.add(f"MATCH (n")

        if req.get_properties() is not None:
            properties = dict((x, y) for x, y in req.get_properties().items() if y != "")
            if len(properties) > 0:
                builder.add_parameters(properties)

        builder.add(")")

        if req.get_relationships() is not None:
            counter: int = 0
            for key, value in req.get_relationships().items():
                if len(value) > 0:
                    builder.add(f"MATCH (n)-[r{counter}:{key}]-(m{counter}) WHERE ID(m{counter}) IN {str(value)}")
                    counter += 1
        builder.add("RETURN COLLECT(ID(n)) AS ids")

        records = self._exec_query(builder.get())[0]
        result_nodes: List[Node] = []  # nodes from result
        if len(records) > 0:
            for record in records:
                result_node = self.get_node_by_id(int(record))
                result_nodes.append(result_node[0])

        return result_nodes

    def get_node_by_id(self, node_id: int) -> Optional[List[Node]]:
        builder = QueryBuilder()
        builder.match_by_id(node_id, "n").add("RETURN n")
        result = self._exec_query(builder.get())

        if len(result) <= 0:
            return None
        record: Neo4jNode = result[0]

        node_type: OType = self.extract_node_type(record.labels)
        if node_type is None:
            return None

        properties: Dict[str, str] = dict().fromkeys(node_type.properties, "")
        for key, value in record.items():
            properties.update({key: value})

        builder = QueryBuilder()
        builder.add(f"MATCH (n)-[r]-(m) WHERE ID(n)={node_id} RETURN TYPE(r) as name, COLLECT(ID(m)) as ids")
        records = self._exec_query(builder.get(), single=False)

        relationships = {rel: set() for rel in node_type.relationships}
        if records is not None and len(records) > 0:
            for record in records:
                relationships.update({record.get('name'): set(record.get('ids'))})

        result_node = self.compose_node(node_type, node_id, properties, relationships)
        return [result_node]

    def extract_node_type(self, labels: List[str]) -> Optional[OType]:
        otypes: List[OType] = [self._ontology.get_type(str(x)) for x in labels]
        meta_union: Set[str] = set().union(*[x.meta for x in otypes])
        node_type: OType = None
        for otype in otypes:
            if otype.entity not in meta_union:
                node_type = otype
                break
        return node_type

    def update_node(self, req: Node) -> Optional[Node]:
        if req.get_properties() is not None:
            properties = dict((x, y) for x, y in req.get_properties().items() if y != "")
            if len(properties) > 0:
                builder = QueryBuilder()
                builder.match_by_id(req.get_id(), "n").set_values(req.get_properties(), "n").add("RETURN n")
                _ = self._exec_query(builder.get())

        if req.get_relationships() is not None:
            relationships = dict((x, y) for x, y in req.get_relationships().items() if len(y) > 0)
            if len(relationships) > 0:
                builder = QueryBuilder()
                builder.match_by_id(req.get_id(), "n")

                counter: int = 0
                for _, value in relationships.items():
                    builder.add(f"MATCH (m{counter}) WHERE ID(m{counter}) IN [{','.join((str(rel) for rel in value))}] ")
                    counter += 1
                counter = 0
                for key, _ in relationships.items():
                    builder.add(f"MERGE (n)-[r{counter}:{key}]-(m{counter})")
                    counter += 1
                builder.add("RETURN n")

                _ = self._exec_query(builder.get())

        result_node = self.get_node_by_id(req.get_id())[0]  # node from result
        return result_node

    def delete_properties_relationships(self, req: Node) -> bool:
        response = False

        if req.get_properties() is not None:
            properties = dict((x, y) for x, y in req.get_properties().items() if y != "")
            if len(properties) > 0:
                builder = QueryBuilder()
                builder.match_by_id(req.get_id(), "n")

                for key, _ in properties.items():
                    if key != "name":
                        builder.add(f"REMOVE n.{key}")
                builder.add("RETURN n")

                result = self._exec_query(builder.get())
                if result:
                    response = True

        if req.get_relationships() is not None:
            relationships = dict((x, y) for x, y in req.get_relationships().items() if len(y) > 0)
            if len(relationships) > 0:
                builder = QueryBuilder()
                builder.match_by_id(req.get_id(), "n")

                counter: int = 0
                for key, value in relationships.items():
                    builder.add(f"MATCH (n)-[r{counter}:{key}]-(m{counter}) WHERE ID(m{counter}) IN {value}")
                    counter += 1
                counter -= 1
                builder.add(f"DELETE r{counter}")
                while counter > 0:
                    counter -= 1
                    builder.add(f",r{counter}")
                builder.add("RETURN n")

                result = self._exec_query(builder.get())
                if result:
                    response = True

        return response

    def delete_node(self, node_id: int) -> bool:
        query = ""  # builder from MNM
        self._exec_query(query)
        if self.get_node_by_id(node_id) is None:
            return True
        else:
            return False

    def compose_node(self, otype: OType, node_id: int, properties: Dict[str, str], relationships: Dict[str, Set[int]]):
        new_node: Node = Node(metatype=otype)
        new_node.set_id(node_id)
        new_node.set_properties(properties)
        new_node.set_relationships(relationships)
        return new_node
