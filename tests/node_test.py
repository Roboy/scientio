from src.scientio.node import Node
from src.scientio.node import RelationshipAvailability
from src.scientio.concept import Concept

import pytest

@pytest.fixture
def empty_node():
    return Node()

@pytest.fixture
def full_node():
	node = Node(None, "Person")
	node.set_id(3)
	properties = {"name": "Negin", "sex": "female"}
	node.set_properties(**properties)
	relationships = {"FROM": 10, "STUDY_AT": 14, "HAS_HOBBY": [16, 25]}
	node.set_relationships(**relationships)
	return node

@pytest.fixture
def equal_node(full_node: Node):
	node = Node(full_node, "Person")
	return node

def test_empty_node(empty_node: Node):
	errors = []
	if not empty_node.get_id() == 0:
		errors.append("node ID is not on default value.")
	if not empty_node.get_concept() == None:
		errors.append("node concept is not on default value.")
	if not len(empty_node.get_concepts()) == 0:
		errors.append("node concepts are not on default vaule.")
	if not len(empty_node.get_properties()) == 0:
		errors.append("node properties are not on default value.")
	if not len(empty_node.get_relationships()) == 0:
		errors.append("node relationships are not on defaul value.")
	assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_full_node(full_node: Node):
	errors = []
	if not full_node.get_id() == 3:
		errors.append("Get node ID resulted in wrong value.")
	
	if not full_node.get_concept() == "Person":
		errors.append("Get node concept resulted in wrong value.")
	if not full_node.get_properties("sex") == "female":
		errors.append("Get node property by key resulted in wrong value.")
	if not full_node.get_properties() == full_node.properties:
		errors.append("Get all property information resulted in a wrong dict.")
	if not full_node.get_relationships("FROM") == [10]:
		errors.append("Get relationship by key resulted in wrong value.")
	if not full_node.get_relationships() == full_node.relationships:
		errors.append("Get all relationship information resulted in wrong dict.")
	if not full_node.has_relationships("STUDY_AT"):
		errors.append("Checking for specific relationship failed.")
	if not full_node.get_name() == "Negin":
		errors.append("Checking name property failed.")
	assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_reset_node(full_node: Node):
	full_node.reset_node()
	errors = []
	if not full_node.get_id() == 0:
		errors.append("node ID is not on default value.")
	if not full_node.get_concept() == None:
		errors.append("node concept is not on default value.")
	if not len(full_node.get_concepts()) == 0:
		errors.append("node concepts are not on default vaule.")
	if not len(full_node.get_properties()) == 0:
		errors.append("node properties are not on default value.")
	if not len(full_node.get_relationships()) == 0:
		errors.append("node relationships are not on defaul value.")
	assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_relationship_availability(full_node: Node):
	errors = []
	all_available = ["FROM", "STUDY_AT", "HAS_HOBBY"]
	some_available = ["FROM", "STUDY_AT", "FRIEND_OF"]
	none_available = ["SIBLING_OF", "FRIEND_OF"]
	if not full_node.check_relationship_availability(all_available) == RelationshipAvailability.ALL_AVAILABLE:
		errors.append("Checking if all of these relationships are available failed.")
	if not full_node.check_relationship_availability(some_available) == RelationshipAvailability.SOME_AVAILABLE:
		errors.append("Checking if some of these relationships are available failed.")
	if not full_node.check_relationship_availability(none_available) == RelationshipAvailability.NONE_AVAILABLE:
		errors.append("Checking if none of these relationships are available failed.")
	assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_purity_relationships(full_node: Node):
	relationships = ["FROM", "FRIEND_OF", "STUDY_AT", "HAS_HOBBY", "SIBLING_OF"]
	purity = {False:["FRIEND_OF", "SIBLING_OF"], True:["FROM", "STUDY_AT", "HAS_HOBBY"]}
	assert full_node.get_purity_relationships(relationships) == purity

def test_equality(full_node: Node, equal_node: Node):
	errors = []
	if not full_node.get_id() == equal_node.get_id():
		errors.append("ID not equal.")
	if not full_node.get_concept() == equal_node.get_concept():
		errors.append("Concept not equal.")
	if not full_node.get_concepts() == equal_node.get_concepts():
		errors.append("Concepts not equal.")
	if not full_node.get_properties() == equal_node.get_properties():
		errors.append("Properties not equal.")
	if not full_node.get_relationships() == equal_node.get_relationships():
		errors.append("Relationships not equal.")
	if not full_node == equal_node:
		errors.append("Equality operator does not work.")
	if not hash(full_node) == hash(equal_node):
		errors.append("Hash does not work.")
	assert not errors, "errors occured:\n{}".format("\n".join(errors))


