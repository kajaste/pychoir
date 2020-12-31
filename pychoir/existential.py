from typing import Any, Iterable

from pychoir.core import Matchable, Matcher


class Anything(Matcher):
    """A Matcher that matches anything.

    Usage:
      >>> from pychoir import Anything
      >>> None == Anything()
      True
      >>> {'a': None} == {'a': Anything()}
      True
      >>> {'b': 1} == {'a': Anything()}
      False
    """
    def _matches(self, _: Any) -> bool:
        return True

    def _description(self) -> str:
        return ''


class Is(Matcher):
    """A Matcher checking that the compared value :code:`is` the passed value.

    In Python :code:`is` is used to check whether two objects are the same object in memory.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import Is
      >>> None == Is(None)
      True
      >>> [] == Is([])
      False
    """
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return other is self.value

    def _description(self) -> str:
        return repr(self.value)


class IsNoneOr(Matcher):
    """A Matcher checking that the compared value :code:`is None` or equal to the passed value.

    This is useful for checking :code:`Optional` values.

    :param matchers: The value(s) and/or matcher(s) to compare against.

    Usage:
      >>> from pychoir import IsNoneOr
      >>> None == IsNoneOr(5)
      True
      >>> 5 == IsNoneOr(5)
      True
      >>> 4 == IsNoneOr(5)
      False
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return other is None or any(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


Optionally = IsNoneOr


class IsTruthy(Matcher):
    """A Matcher checking that the compared value is *truthy* when used as a condition.

    In other words, checks whether :code:`if value: ... else: ...` would go to the if branch.

    Usage:
      >>> from pychoir import IsTruthy
      >>> '' == IsTruthy()
      False
      >>> 5 == IsTruthy()
      True
    """
    def _matches(self, other: Any) -> bool:
        return bool(other)

    def _description(self) -> str:
        return ''


class IsFalsy(Matcher):
    """A Matcher checking that the compared value is *falsy* when used as a condition.

    In other words, checks whether :code:`if value: ... else: ...` would go to the else branch.

    Usage:
      >>> from pychoir import IsFalsy
      >>> '' == IsFalsy()
      True
      >>> 5 == IsFalsy()
      False
    """
    def _matches(self, other: Any) -> bool:
        return not bool(other)

    def _description(self) -> str:
        return ''


class In(Matcher):
    """A Matcher checking that the compared value is in the passed iterable.

    Usage:
      >>> from string import ascii_lowercase
      >>> from pychoir import In
      >>> 'a' == In(ascii_lowercase)
      True
      >>> 'A' == In(ascii_lowercase)
      False
    """
    def __init__(self, allowed_values: Iterable[Any]):
        super().__init__()
        self.allowed_values = allowed_values

    def _matches(self, other: Any) -> bool:
        return other in self.allowed_values

    def _description(self) -> str:
        return repr(self.allowed_values)


OneOf = In
