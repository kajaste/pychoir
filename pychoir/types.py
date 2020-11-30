from typing import Any, Type

from pychoir.core import Matcher


class IsInstance(Matcher):
    def __init__(self, type_: Type[Any]):
        self.type = type_

    def matches(self, other: Any) -> bool:
        return isinstance(other, self.type)

    def description(self) -> str:
        return f'{self.type.__name__}'


OfType = IsInstance
