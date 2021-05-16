from typing import Any, Callable

from pychoir.core import Matchable, Matcher


class And(Matcher):
    """A Matcher checking that the compared value matches *all* the passed :class:`Matchable` s.

    :param matchers: The value(s) and/or matcher(s) to compare against.

    Usage:
      >>> from pychoir import And, IsInstance, HasLength, StartsWith
      >>> 5 == And(IsInstance(int), 5)
      True
      >>> 'abc' == And(StartsWith('a'), HasLength(3))
      True
      >>> 4 == And(IsInstance(int), 5)
      False
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return all(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AllOf = And


class Or(Matcher):
    """A Matcher checking that the compared value matches *at least one of* the passed :class:`Matchable` s.

    :param matchers: The value(s) and/or matcher(s) to compare against.

    Usage:
      >>> from pychoir import Or, IsInstance, StartsWith
      >>> 5 == Or(IsInstance(int), 5)
      True
      >>> 'abc' == Or(StartsWith('abc'), StartsWith('def'))
      True
      >>> '4' == Or(IsInstance(int), 5)
      False
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return any(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AnyOf = Or


class Not(Matcher):
    """A Matcher checking that the compared value matches *none of* the passed :class:`Matchable` s.

    :param matchers: The value(s) and/or matcher(s) to compare against.

    Usage:
      >>> from pychoir import Not, IsInstance, StartsWith
      >>> 5 == Not(IsInstance(str))
      True
      >>> 'abc' == Not(StartsWith('abc'), StartsWith('def'))
      False
      >>> 4 == Not(IsInstance(str), 5)
      True
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return not any(self.nested_match(matcher, other, expect_mismatch=True) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


IsNoneOf = Not


class ResultsTrueFor(Matcher):
    """A Matcher checking that the compared value results :code:`True` when given to the passed function(s).

    :param conditions: The functions to check against.

    Usage:
      >>> from pychoir import ResultsTrueFor
      >>> 5 == ResultsTrueFor(bool)
      True
      >>> 'abc' == ResultsTrueFor(lambda x: x[2] == 'c')
      True
    """
    def __init__(self, *conditions: Callable[[Any], bool]):
        super().__init__()
        self.conditions = conditions

    def _matches(self, other: Any) -> bool:
        return all(condition(other) for condition in self.conditions)

    def _description(self) -> str:
        return ', '.join(map(repr, self.conditions))
