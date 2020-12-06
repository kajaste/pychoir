from typing import Any, Iterable

from pychoir.core import Matchable, Matcher


class Anything(Matcher):
    def _matches(self, _: Any) -> bool:
        return True

    def _description(self) -> str:
        return ''


class Is(Matcher):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return other is self.value

    def _description(self) -> str:
        return repr(self.value)


class IsNoneOr(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return other is None or any(self.nested_match(matcher, other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


Optionally = IsNoneOr


class IsTruthy(Matcher):
    def _matches(self, other: Any) -> bool:
        return bool(other)

    def _description(self) -> str:
        return ''


class IsFalsy(Matcher):
    def _matches(self, other: Any) -> bool:
        return not bool(other)

    def _description(self) -> str:
        return ''


class In(Matcher):
    def __init__(self, allowed_values: Iterable[Any]):
        super().__init__()
        self.allowed_values = allowed_values

    def _matches(self, other: Any) -> bool:
        return other in self.allowed_values

    def _description(self) -> str:
        return repr(self.allowed_values)


OneOf = In
