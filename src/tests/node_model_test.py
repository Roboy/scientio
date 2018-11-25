import pytest

from src.scientio.node_model import NodeModel
from src.scientio.label import Label

@pytest.fixture
def empty_node():
    return NodeModel()

def test_default_node(empty_node:NodeModel):
    assert empty_node.id == 0

def test_set_id(empty_node:NodeModel):
    empty_node.set_id(5)
    assert empty_node.get_id() == 5

def test_set_label_single(empty_node:NodeModel):
    label = Label()
    empty_node.set_label(label)
    assert empty_node.get_label() == label 

def test_set_label_multiple(empty_node:NodeModel):
    labels = set()
    labels.add(Label())
    labels.add(Label())
    empty_node.set_label(labels)
    assert empty_node.get_labels() == labels

def test_set_label_error(empty_node:NodeModel):
    with pytest.raises(TypeError): 
        empty_node.set_label(5)

def test_set_properies_single(empty_node:NodeModel):
    prop1 = Neo4jProperty.name
    info = "Negin"
    empty_node.set_properties(prop1, info)
    assert empty_node.get_properties(prop1) == info 

def test_set_properties_multiple(empty_node:NodeModel):
    prop1 = Neo4jProperty.name
    prop2 = Neo4jProperty.sex
    properties = dict()
    properties[prop1] = "Negin"
    properties[prop2] = "female"
    empty_node.set_properties(properties)
    assert empty_node.get_properties() == properties

def test_set_properties_error(empty_node:NodeModel):
    with pytest.raises(TypeError): 
        empty_node.set_properties(5)

def test_set_relationships_single(empty_node:NodeModel):
    relation = Neo4jRelationship.FROM
    info = "Munich"
    empty_node.set_relationships(relation, info)
    assert empty_node.get_relationships(relation) == info
