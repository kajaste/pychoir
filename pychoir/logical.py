from typing import Any, Callable

from pychoir.core import Matchable, Matcher


class And(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return all(Matcher.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AllOf = And


class Or(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return any(Matcher.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AnyOf = Or


class Not(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return all(Matcher.nested_match(matcher, other, inverse=True) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


IsNoneOf = Not


class ResultsTrueFor(Matcher):
    def __init__(self, condition: Callable[[Any], bool]):
        super().__init__()
        self.condition = condition

    def _matches(self, other: Any) -> bool:
        return self.condition(other)

    def _description(self) -> str:
        return repr(self.condition)
