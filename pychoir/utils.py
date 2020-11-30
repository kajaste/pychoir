"""
Useful extensions for standard library
"""
from typing import Sequence, TypeVar, Union

T = TypeVar('T')


def sequence_or_its_only_member(sequence: Sequence[T]) -> Union[Sequence[T], T]:
    if len(sequence) == 1:
        return sequence[0]
    else:
        return sequence
