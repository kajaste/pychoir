import sys
from abc import ABC, abstractmethod
from typing import Any, Callable, Type, TypeVar

MatchedType = TypeVar('MatchedType', bound=Any)

if sys.version_info >= (3, 8):
    from typing import Protocol

    class Matchable(Protocol):
        def __eq__(self, other: MatchedType) -> bool:
            ...  # pragma: no cover
else:
    Matchable = Any


if sys.version_info >= (3, 8):
    from typing import final
else:
    CallableT = TypeVar('CallableT', bound=Callable)

    def final(x: CallableT) -> CallableT:
        return x


T = TypeVar('T')


class Matcher(ABC):
    @abstractmethod
    def matches(self, other: MatchedType) -> bool:
        ...  # pragma: no cover

    @abstractmethod
    def description(self) -> str:
        ...  # pragma: no cover

    def as_(self, _: Type[T]) -> T:
        """To make matchers pass type checking"""
        return self  # type: ignore

    @final
    def __eq__(self, other: MatchedType) -> bool:
        return self.matches(other)

    @final
    def __ne__(self, other: MatchedType) -> bool:
        return not self.matches(other)

    @final
    def __str__(self) -> str:
        return self.description()

    @final
    def __repr__(self) -> str:
        return self.description()
