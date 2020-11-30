from typing import Any, Callable

from pychoir.core import Matchable, Matcher


class And(Matcher):
    def __init__(self, *matchers: Matchable):
        self.matchers = matchers

    def matches(self, other: Any) -> bool:
        return all(matcher == other for matcher in self.matchers)

    def description(self) -> str:
        return f'{", ".join(map(repr, self.matchers))}'


AllOf = And


class Or(Matcher):
    def __init__(self, *matchers: Matchable):
        self.matchers = matchers

    def matches(self, other: Any) -> bool:
        return any(matcher == other for matcher in self.matchers)

    def description(self) -> str:
        return f'{", ".join(map(repr, self.matchers))}'


AnyOf = Or


class Not(Matcher):
    def __init__(self, *matchers: Matchable):
        self.matchers = matchers

    def matches(self, other: Any) -> bool:
        return not any(matcher == other for matcher in self.matchers)

    def description(self) -> str:
        return f'{", ".join(map(repr, self.matchers))}'


IsNoneOf = Not


class ResultsTrueFor(Matcher):
    def __init__(self, condition: Callable[[Any], bool]):
        self.condition = condition

    def matches(self, other: Any) -> bool:
        return self.condition(other)

    def description(self) -> str:
        return f'{self.condition!r}'
