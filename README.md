# Roboy ScientIO

## About

Roboy ScientIO (from Lat. scientia - knowledge and Input/Output) - a Knowledge Graph Engine to organise and query complex data.

## Dependencies

To use ScientIO, you will need to have one of it's supported back-ends installed. Currently, the only supported back-end is Neo4j, which may be run in a number of ways
(if you don't have a remote instance available). We recommend simply running it through docker - like this:

```bash
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/neo4j/logs:/logs \
    neo4j:3.0
```

## Installation

### Via PIP

The easiest way to install ScientIO is through pip:

``
pip install scientio
``

### For developers

First, install dependencies:

```bash
pip install -r requirements.txt
```

Then, you may open the repository in any IDE, and mark the
`src` folder as a sources root.

## Basic ScientIO use-cases

### Supplying an ontology description

The ontology description is a collection of named entity types, where each type may declare a specific set of properties and relationships like this:

```yaml
# my_ontology.yml

!OType
entity: Alien    # The name of the ontology type
---
!OType
entity: Vulcan   # Declare a more specific Alien type
meta: [Alien]
properties:      # Allowed properties for every Vulcan
 - name
 - homeworld
 - ear_pointiness
---
!OType
entity: Human    # Declare a more specific Alien type
meta: [Alien]
properties:      # Allowed properties for every Human
 - name
 - homeworld
relationships: [captain_of]  # Allowed relationships for every Human
```

### Creating some nodes

```python
from scientio.ontology.ontology import Ontology
from scientio.session import Session
from scientio.ontology.node import Node

# Load the ontology from a yaml file
onto = Ontology(path_to_yaml="my_ontology.yml")

# Create a session (with default Neo4j backend)
sess = Session(
    ontology=onto,
    neo4j_address="bolt://localhost:7687",
    neo4j_username="neo4j",
    neo4j_password="test")

# Get human/vulcan types from ontology
human_type = onto.get_type("Human")
vulcan_type = onto.get_type("Vulcan")

# Create a transient human named "Kirk"
kirk = Node(metatype=human_type)
kirk.set_name("Kirk")

# Create a transient vulcan named "Spock"
spock = Node(metatype=vulcan_type)
spock.set_name("Spock")

# Persist kirk and spock
sess.create(kirk)
sess.create(spock)
```

### Add a relationship between your nodes

```python
from scientio.ontology.ontology import Ontology
from scientio.session import Session
from scientio.ontology.node import Node

# Load the ontology from a yaml file
onto = Ontology(path_to_yaml="my_ontology.yml")

# Create a session (with default Neo4j backend)
sess = Session(
    ontology=onto,
    neo4j_address="bolt://localhost:7687",
    neo4j_username="neo4j",
    neo4j_password="test")

# Get human/vulcan types from ontology
human_type = onto.get_type("Human")
vulcan_type = onto.get_type("Vulcan")

# Create query templates to get the actual kirk/spock
kirk = Node(metatype=human_type)
spock = Node(metatype=vulcan_type)

# Query Kirk and Spock from the database, using
# the query nodes we created previously. We're just
# gonna assume that the first human is Kirk, and the first
# vulcan is Spock.
kirk = sess.retrieve(request=kirk)[0]
spock = sess.retrieve(request=spock)[0]

# Add a relationship between Kirk and Spock
kirk.add_relationship({"captain_of": {spock.get_id()}})

# Make sure that the new relationship is persisted
sess.update(kirk)
```
