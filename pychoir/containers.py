import sys
from typing import Any, Iterable, Mapping

from pychoir.core import Matchable, Matcher

if sys.version_info >= (3, 8):
    from typing import Protocol

    class Lengthy(Protocol):
        def __len__(self) -> int:
            ...  # pragma: no cover
else:
    Lengthy = Any


class IsEmpty(Matcher):
    """A Matcher checking that the `len()` of the compared value is 0.

    Usage:
      >> from pychoir import All, IsEmpty, Not
      >> ('', [], {}, set(), tuple()) == All(IsEmpty())
      True
      >> {'not': 'empty'} == Not(IsEmpty())
      True
    """

    def _matches(self, other: Lengthy) -> bool:
        return len(other) == 0

    def _description(self) -> str:
        return ''


class HasLength(Matcher):
    """A Matcher checking that the `len()` of the compared value matches the passed Matchable.

    :param matcher: The value or Matcher to compare against.

    Usage:
      >>> from pychoir import GreaterThan, HasLength
      >>> 'foo' == HasLength(3)
      True
      >>> 'foo' == HasLength(GreaterThan(2))
      True
    """
    def __init__(self, matcher: Matchable):
        super().__init__()
        self.matcher = matcher

    def _matches(self, other: Lengthy) -> bool:
        return self.nested_match(self.matcher, len(other))

    def _description(self) -> str:
        return repr(self.matcher)


Len = HasLength


class All(Matcher):
    """A Matcher checking that all values in a container match passed Matchables.

    :param matchers: The value(s) and/or Matcher(s) to compare against.

    Usage:
      >>> from pychoir import All, IsInstance
      >>> 'aaa' == All('a')
      True
      >>> [1, 2, 3] == All(IsInstance(int))
      True
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return all(self.nested_match(matcher, value) for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class AreNot(Matcher):
    """A Matcher checking that none of the values in a container match passed Matchables.

    :param matchers: The value(s) and/or Matcher(s) to compare against.

    Usage:
      >>> from pychoir import AreNot, IsInstance
      >>> 'abc' == AreNot('a', 'b')
      False
      >>> [1, 2, 3] == AreNot(IsInstance(str))
      True
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return not any(self.nested_match(matcher, value, expect_mismatch=True)
                       for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class ContainsAllOf(Matcher):
    """A Matcher checking that a container contains *at least* the passed values.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsAllOf
      >>> 'abc' == ContainsAllOf('a', 'b')
      True
      >>> [1, 2, 3] == ContainsAllOf(3, 4)
      False
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return all(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsAnyOf(Matcher):
    """A Matcher checking that a container contains *at least one of* the passed values.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsAnyOf
      >>> 'abc' == ContainsAnyOf('a', 'b')
      True
      >>> [1, 2, 3] == ContainsAnyOf(3, 4)
      True
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsNoneOf(Matcher):
    """A Matcher checking that a container contains none of the passed values.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsNoneOf
      >>> 'abc' == ContainsNoneOf('a', 'b')
      False
      >>> [1, 2, 3] == ContainsNoneOf(4)
      True
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return not any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class DictContainsAllOf(Matcher):
    """A Matcher checking that a Mapping contains *at least* the passed Mapping.
    Usually this means that the passed dict is a subset of the one compared against.
    Keys expected to be absent can be set as :class:`NotPresent`.

    :param value: The Mapping to find in the Mapping compared against.

    Usage:
      >>> from pychoir import DictContainsAllOf, NotPresent
      >>> {'a': 1, 'b': 2, 'd': 3} == DictContainsAllOf({'a': 1, 'c': NotPresent})
      True
      >>> {'a': 1, 'c': 2, 'd': 3} == DictContainsAllOf({'a': 1, 'c': NotPresent})
      False
    """
    def __init__(self, value: Mapping[Any, Any]):
        super().__init__()
        self.expected = value

    def _matches(self, other: Mapping[Any, Any]) -> bool:
        match_dict = {key: value for key, value in other.items() if key in self.expected}
        for key in self.expected:
            if key not in match_dict:
                match_dict[key] = NotPresent
        return self.expected == match_dict

    def _description(self) -> str:
        return repr(self.expected)


class _NotPresent:
    def __str__(self) -> str:
        return 'NotPresent'

    def __repr__(self) -> str:
        return str(self)


NotPresent = _NotPresent()


class IsNotPresentOr(Matcher):
    """A Matcher checking that a value is either :class:`NotPresent` or matches the passed matcher.
    Usually used for example with :class:`DictContainsAllOf`.

    :param matcher: The Mapping to find in the Mapping compared against.

    Usage:
      >>> from pychoir import DictContainsAllOf, IsNotPresentOr
      >>> {'a': 2} == DictContainsAllOf({'a': IsNotPresentOr(2)})
      True
      >>> {} == DictContainsAllOf({'a': IsNotPresentOr(2)})
      True
    """
    def __init__(self, matcher: Matchable):
        super().__init__()
        self.matcher = matcher

    def _matches(self, other: Any) -> bool:
        return other is NotPresent or self.nested_match(self.matcher, other)

    def _description(self) -> str:
        return repr(self.matcher)
