from typing import Any, Iterable

from pychoir.core import Matchable, Matcher


class _Anything(Matcher):
    def matches(self, _: Any) -> bool:
        return True

    def description(self) -> str:
        return 'Anything'


Anything = _Anything()


class Is(Matcher):
    def __init__(self, value: Any):
        self.value = value

    def matches(self, other: Any) -> bool:
        return other is self.value

    def description(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'


class IsNoneOr(Matcher):
    def __init__(self, *matchers: Matchable):
        self.matchers = matchers

    def matches(self, other: Any) -> bool:
        return other is None or any(other == matcher for matcher in self.matchers)

    def description(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(repr, self.matchers))})'


Optionally = IsNoneOr


class _IsTruthy(Matcher):
    def matches(self, other: Any) -> bool:
        return bool(other)

    def description(self) -> str:
        return 'IsTruthy'


IsTruthy = _IsTruthy()


class _IsFalsy(Matcher):
    def matches(self, other: Any) -> bool:
        return not bool(other)

    def description(self) -> str:
        return 'IsFalsy'


IsFalsy = _IsFalsy()


class In(Matcher):
    def __init__(self, allowed_values: Iterable[Any]):
        self.allowed_values = allowed_values
        self.allowed_values_set = allowed_values

    def matches(self, other: Any) -> bool:
        return other in self.allowed_values_set

    def description(self) -> str:
        return f'{self.__class__.__name__}({self.allowed_values!r})'


OneOf = In
