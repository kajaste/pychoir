from typing import Any, Callable

from pychoir.core import Matchable, Matcher


class And(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return all(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AllOf = And


class Or(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return any(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


AnyOf = Or


class Not(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return all(self.nested_match(matcher, other, inverse=True) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


IsNoneOf = Not


class ResultsTrueFor(Matcher):
    def __init__(self, *conditions: Callable[[Any], bool]):
        super().__init__()
        self.conditions = conditions

    def _matches(self, other: Any) -> bool:
        return all(condition(other) for condition in self.conditions)

    def _description(self) -> str:
        return ', '.join(map(repr, self.conditions))
