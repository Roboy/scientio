from typing import Any
from ..config import STYLE


class OField(object):

    def __init__(self, value: str, style: str = None):
        self.value: str = self._styler(value, STYLE if style is None else style)

    def __eq__(self, o: object) -> bool:
        return type(o) == OField and o.value == self.value

    def _styler(self, value: str, style: str) -> str:
        if style == "upper":
            return value.upper()
        elif style == "lower":
            return value.lower()
        elif style == "cap":
            return value.capitalize()
        else:
            return value

    def upper(self) -> Any:
        if type(self.value) == str:
            self.value = self.value.upper()
        return self.value

    def lower(self) -> Any:
        if type(self.value) == str:
            self.value = self.value.lower()
        return self.value

    def capitalize(self) -> Any:
        if type(self.value) == str:
            self.value = self.value.capitalize()
        return self.value

    def to_int(self) -> int:
        try:
            self.value = int(self.value)
            return self.value
        except ValueError:
            return None

    def to_float(self) -> float:
        try:
            self.value = float(self.value)
            return self.value
        except ValueError:
            return None

    def to_date(self):
        pass




