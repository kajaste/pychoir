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


class HasLength(Matcher):
    def __init__(self, matcher: Matchable):
        super().__init__()
        self.matcher = matcher

    def _matches(self, other: Lengthy) -> bool:
        return self.nested_match(self.matcher, len(other))

    def _description(self) -> str:
        return repr(self.matcher)


Len = HasLength


class All(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return all(self.nested_match(matcher, value) for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class AreNot(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return all(self.nested_match(matcher, value, inverse=True)
                   for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class ContainsAllOf(Matcher):
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return all(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsAnyOf(Matcher):
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsNoneOf(Matcher):
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return not any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class DictContainsAllOf(Matcher):
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
    pass


NotPresent = _NotPresent()


class IsNotPresentOr(Matcher):
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: Any) -> bool:
        return other is NotPresent or any(matcher == other for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))
