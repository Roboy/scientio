from . ontology import Ontology
from . operations import Operations
from . node_model import NodeModel
import sys


class Session(Operations):

    _driver: Operations

    def __init__(self, *, driver_name: str="drivers.Neo4j", ontology: Ontology, **kwargs):
        pass

    def create(self, request: NodeModel) -> NodeModel:
        return self._driver.create(request)

    def retrieve(self, request: NodeModel, node_id: int = None) -> NodeModel:
        return self._driver.retrieve(request, node_id)

    def update(self, request: NodeModel) -> NodeModel:
        return self._driver.update(request)

    def delete(self, request: NodeModel) -> bool:
        return self._driver.delete(request)

    @staticmethod
    def _driver_for_name(self, driver_name: str):
        driver = getattr(sys.modules[__name__], driver_name)
        if not driver:
            raise KeyError(driver_name)
        return driver