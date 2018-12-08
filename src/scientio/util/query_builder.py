import re
import string
from typing import Dict, List, Any


class QueryBuilder(object):
    """
    Creates a valid OpenCypher query based on arguments, properties and parameters
    Sample usages:
    * builder.matchById(id, "n").add("RETURN PROPERTIES(n)").get() ->
        "MATCH (n) WHERE ID(n)=id RETURN PROPERTIES(n)"
    * builder.add("MATCH (n:%s", get.getLabel()).add_parameters(get.getProperties()).add(")")
      builder.add("RETURN COLLECT(ID(n)) AS ids").get() ->
        "MATCH (n:Roboy) {name:'roboy'} RETURN COLLECT(ID(n)) AS ids"

    TODO: Break down builder.add("MATCH (n)-[r]-(m) WHERE ID(n)=%d RETURN TYPE(r) as name, COLLECT(ID(m)) as ids", id)

    """
    query: string = ''  # String storing a Cypher query

    def __init__(self, query: string = None, builder: 'QueryBuilder' = None):
        """
        Initialise a QueryBuilder object
        If query is None and builder is None, initialises an empty QueryBuilder.
        If builder is not None, acts as a copy constructor.
        If builder is None and query is not None, initialises self.query string with the input.
        :param query: string containing a Cypher query
        :param builder: a QueryBuilder object
        """
        if builder is not None:
            self.query = builder.query
        elif query is not None:
            self.query = query
        else:
            self.query = ''

    def get(self) -> str:
        """
        Access the query string representation
        :return: string representing a query
        """
        return re.sub("\s\s+", " ", self.query.strip())

    def append(self, chunks: List[str]) -> 'QueryBuilder':
        """
        Attach several parts of the query together
        :param parts: list of strings
        :return: this QueryBuilder
        """
        self.query += "".join(chunks)
        return self

    def add(self, chunk: str) -> 'QueryBuilder':
        """
        Add a single token/call into the Cypher query
        :param chunk: string containing a single part of the query
        :return: this QueryBuilder
        """
        return self.append([" ", chunk, " "])

    def add_meta(self, meta: List[str]) -> 'QueryBuilder':
        """
        Add a single token/call into the Cypher query
        :param meta: frozenset containing meta of the node
        :return: this QueryBuilder
        """
        return self.add(":".join(meta))

    def format(self, chunk: str, *args: List[Any]) -> 'QueryBuilder':
        """
        Add arguments into the Cypher query string
        :param chunk: token/call defining the list of objects
        :param args: list of objects to be added to the token
        :return: this QueryBuilder
        """
        return self.add(chunk.format(*args))

    def add_parameters(self, properties: Dict[str, str]) -> 'QueryBuilder':
        """
        Add the node properties to the Cypher query
        :param properties: properties of the node
        :return: this QueryBuilder
        """
        param_list: [str] = []
        for key, value in properties.items():
            param_list.append(f"{key}: '{value}'")
        return self.add(f"{{{', '.join(param_list)}}}")

    def match_by_id(self, id: int, letter: str) -> 'QueryBuilder':
        """
        Match the ID to the node variable in the Cypher query
        :param id: a number denoting the ID of the node in the DB
        :param letter: a variable identifying the node in the Cypher query
        :return: this QueryBuilder
        """
        return self.add(f"MATCH ({letter}) WHERE ID({letter})={id}")

    def set_values(self, properties: Dict[str, str], letter: str) -> 'QueryBuilder':
        """
        Create Cypher SET query to set the value to the node in the query
        :param properties: properties that have to be initialised
        :param letter: a variable identifying the node in the Cypher query
        :return: this QueryBuilder
        """
        for key, value in properties.items():
            self.add(f"SET {letter}.{key}='{value}'")
        return self
