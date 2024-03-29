from typing import Any, Type

from pychoir.core import Matcher


class IsInstance(Matcher):
    """A Matcher checking that the compared object's type matches the passed one.

    :param types: The expected type(s) of compared values.

    Usage:
      >>> from pychoir import IsInstance
      >>> 5 == IsInstance(int)
      True
      >>> 'foobar' == IsInstance(int)
      False
      >>> 'foobar' == IsInstance(int, str)
      True
    """
    def __init__(self, *types: Type[Any]):
        super().__init__()
        self.types = types

    def _matches(self, other: Any) -> bool:
        return isinstance(other, self.types)

    def _description(self) -> str:
        return ', '.join(map(lambda t: t.__name__, self.types))


OfType = IsInstance


class ConvertsTo(Matcher):
    """A Matcher checking that the compared value can be converted into the passed type.

    :param type_: The type to which conversion shall be attempted.

    Usage:
      >>> from pychoir import ConvertsTo
      >>> '5' == ConvertsTo(int)
      True
      >>> '5.2' == ConvertsTo(int)
      False
    """
    def __init__(self, type_: Type[Any]):
        super().__init__()
        self.type = type_

    def _matches(self, other: Any) -> bool:
        try:
            converted = self.type(other)
        except:  # noqa: E722
            return False
        return isinstance(converted, self.type)

    def _description(self) -> str:
        return self.type.__name__
