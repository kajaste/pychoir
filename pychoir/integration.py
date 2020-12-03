import sys
from typing import Generic, TypeVar

from pychoir.core import Matcher

T = TypeVar('T', contravariant=True)

if sys.version_info >= (3, 8):
    from typing import Protocol

    class MatcherLike(Protocol[T]):
        def matches(self, other: T) -> bool:
            ...  # pragma: no cover
else:
    MatcherLike = Generic


class Matches(Matcher):
    def __init__(self, *matchers: MatcherLike[T]):
        super().__init__()
        self.matchers = matchers

    def _matches(self, other: T) -> bool:
        return any(matcher.matches(other) for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


M = Matches
