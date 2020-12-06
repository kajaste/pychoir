import sys
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, List, Tuple, Type, TypeVar, Union

from pychoir.utils import sequence_or_its_only_member

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


class _MatcherStatus(str, Enum):
    NOT_RUN = 'NOT RUN'
    PASSED = 'PASSED'
    FAILED = 'FAILED'


class _MatcherState:
    def __init__(self, status: _MatcherStatus = _MatcherStatus.NOT_RUN):
        self.__status: _MatcherStatus = status
        self.__failed_values: List[Any] = []

    def update(self, passed: bool, value: Any) -> None:
        if passed:
            self.__add_success()
        else:
            self.__add_failure(value)

    @property
    def status(self) -> _MatcherStatus:
        return self.__status

    @property
    def failed_values(self) -> Tuple[Any, ...]:
        return tuple(self.__failed_values)

    @property
    def was_already_run(self) -> bool:
        return self.status != _MatcherStatus.NOT_RUN

    def __add_failure(self, value: Any) -> None:
        self.__status = _MatcherStatus.FAILED
        self.__failed_values.append(value)

    def __add_success(self) -> None:
        if not self.was_already_run:
            self.__status = _MatcherStatus.PASSED


class _MatcherContext:
    def __init__(self, inverse_match: bool, nested_call: bool) -> None:
        self.__inverse_match = inverse_match
        self.__nested_call = nested_call

    @property
    def inverse_match(self) -> bool:
        return self.__inverse_match

    @property
    def nested_call(self) -> bool:
        return self.__nested_call


class Matcher(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__state = _MatcherState()

    def as_(self, _: Type[T]) -> T:
        """To make matchers pass type checking"""
        return self  # type: ignore

    @final
    def nested_match(
        self,
        matcher: Union['Matcher', Matchable],
        other: MatchedType,
        inverse: bool = False
    ) -> bool:
        """For calling Matchers from inside Matchers"""
        if isinstance(matcher, Matcher):
            return matcher.matches(other, _MatcherContext(inverse_match=inverse, nested_call=True))
        if inverse:
            return matcher != other
        else:
            return matcher == other

    @abstractmethod
    def _matches(self, other: MatchedType) -> bool:
        ...  # pragma: no cover

    @abstractmethod
    def _description(self) -> str:
        ...  # pragma: no cover

    @final
    def matches(self, other: MatchedType, context: _MatcherContext) -> bool:
        passed = self._matches(other)
        if context.inverse_match:
            passed = not passed

        if not context.nested_call and self.__state.was_already_run:
            warnings.warn(f'Erroneous re-run of {self}. Create a new Matcher instance for each use!')

        self.__state.update(passed, other)

        return passed

    @final
    def __eq__(self, other: MatchedType) -> bool:
        return self.matches(other, _MatcherContext(inverse_match=False, nested_call=False))

    @final
    def __ne__(self, other: MatchedType) -> bool:
        return self.matches(other, _MatcherContext(inverse_match=True, nested_call=False))

    @final
    def __str__(self) -> str:
        return self.__describe()

    @final
    def __repr__(self) -> str:
        return self.__describe()

    @final
    def __describe(self) -> str:
        failed_value = sequence_or_its_only_member(self.__state.failed_values)
        status_str = f'[FAILED for {failed_value!r}]' if self.__state.status == _MatcherStatus.FAILED else ''
        return f'{self.__class__.__name__}({self._description()}){status_str}'
