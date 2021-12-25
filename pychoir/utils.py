"""
Useful extensions for standard library
"""
from enum import Enum
from typing import Any, Sequence, Tuple, TypeVar, Union

T = TypeVar('T')


def sequence_or_its_only_member(sequence: Sequence[T]) -> Union[Sequence[T], T]:
    if len(sequence) == 1:
        return sequence[0]
    else:
        return sequence


def i_removed(tuple_: Tuple[Any, ...], index: Any) -> Tuple[Any, ...]:
    return tuple_[:index] + tuple_[index + 1:]


class DefaultType(Enum):
    DEFAULT = 'default'


Default = DefaultType.DEFAULT
