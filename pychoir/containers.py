import sys
from typing import Any, Iterable, Mapping, Optional, Sequence, Union

from pychoir.core import Matchable, Matcher, Transformer

if sys.version_info >= (3, 8):
    from typing import Protocol

    class Lengthy(Protocol):
        def __len__(self) -> int:
            ...  # pragma: no cover
else:
    Lengthy = Any


class IsEmpty(Matcher):
    """A Matcher checking that the `len()` of the compared value is 0.

    Usage:
      >>> from pychoir import All, IsEmpty, Not
      >>> ('', [], {}, set(), tuple()) == All(IsEmpty())
      True
      >>> {'not': 'empty'} == Not(IsEmpty())
      True
    """

    def _matches(self, other: Lengthy) -> bool:
        return len(other) == 0

    def _description(self) -> str:
        return ''


class HasLength(Matcher):
    """A Matcher checking that the `len()` of the compared value matches the passed Matchable.

    :param matcher: The value or Matcher to compare against.

    Usage:
      >>> from pychoir import GreaterThan, HasLength
      >>> 'foo' == HasLength(3)
      True
      >>> 'foo' == HasLength(GreaterThan(2))
      True
    """
    def __init__(self, matcher: Matchable):
        super().__init__()
        self.matcher = matcher

    def _matches(self, other: Lengthy) -> bool:
        return self.nested_match(self.matcher, len(other))

    def _description(self) -> str:
        return repr(self.matcher)


Len = HasLength


class All(Matcher):
    """A Matcher checking that all values in a container match passed Matchables.

    :param matchers: The value(s) and/or Matcher(s) to compare against.

    Usage:
      >>> from pychoir import All, IsInstance
      >>> 'aaa' == All('a')
      True
      >>> [1, 2, 3] == All(IsInstance(int))
      True
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return all(self.nested_match(matcher, value) for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class AreNot(Matcher):
    """A Matcher checking that none of the values in a container match passed Matchables.

    :param matchers: The value(s) and/or Matcher(s) to compare against.

    Usage:
      >>> from pychoir import AreNot, IsInstance
      >>> 'abc' == AreNot('a', 'b')
      False
      >>> [1, 2, 3] == AreNot(IsInstance(str))
      True
    """
    def __init__(self, *matchers: Matchable):
        super().__init__()
        self.matchers = matchers

    def _matches(self, iterable: Iterable[Any]) -> bool:
        return not any(self.nested_match(matcher, value, expect_mismatch=True)
                       for value in iterable for matcher in self.matchers)

    def _description(self) -> str:
        return ', '.join(map(repr, self.matchers))


class Contains(Matcher):
    """A Matcher checking that a container contains the passed value.

    :param value: The value to find in the container.

    Usage:
      >>> from pychoir import Contains
      >>> 'abc' == Contains('a')
      True
      >>> [1, 2, 3] == Contains(4)
      False
    """
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return self.value in other

    def _description(self) -> str:
        return repr(self.value)


class ContainsAllOf(Matcher):
    """A Matcher checking that a container contains *at least* the passed values.

    Plural of :class:`Contains`.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsAllOf
      >>> 'abc' == ContainsAllOf('a', 'b')
      True
      >>> [1, 2, 3] == ContainsAllOf(3, 4)
      False
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return all(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsAnyOf(Matcher):
    """A Matcher checking that a container contains *at least one of* the passed values.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsAnyOf
      >>> 'abc' == ContainsAnyOf('a', 'b')
      True
      >>> [1, 2, 3] == ContainsAnyOf(3, 4)
      True
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class ContainsNoneOf(Matcher):
    """A Matcher checking that a container contains none of the passed values.

    :param values: The value(s) to find in the container.

    Usage:
      >>> from pychoir import ContainsNoneOf
      >>> 'abc' == ContainsNoneOf('a', 'b')
      False
      >>> [1, 2, 3] == ContainsNoneOf(4)
      True
    """
    def __init__(self, *values: Any):
        super().__init__()
        self.values = values

    def _matches(self, other: Any) -> bool:
        return not any(value in other for value in self.values)

    def _description(self) -> str:
        return ', '.join(map(repr, self.values))


class DictContainsAllOf(Matcher):
    """A Matcher checking that a Mapping contains *at least* the passed Mapping.
    Usually this means that the passed dict is a subset of the one compared against.
    Keys expected to be absent can be set as :class:`NotPresent`.

    :param value: The Mapping to find in the Mapping compared against.

    Usage:
      >>> from pychoir import DictContainsAllOf, NotPresent
      >>> {'a': 1, 'b': 2, 'd': 3} == DictContainsAllOf({'a': 1, 'c': NotPresent})
      True
      >>> {'a': 1, 'c': 2, 'd': 3} == DictContainsAllOf({'a': 1, 'c': NotPresent})
      False
    """
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


class InAnyOrder(Matcher):
    """A Matcher checking that an Iterable contains *exactly* the passed items, in any order.

    The Iterable can be for example a list, tuple or set. Items do not need to be hashable.

    :param values: An Iterable containing the expected items, in any order.

    Usage:
      >>> from pychoir import InAnyOrder
      >>> [1, 2, 3, 3] == InAnyOrder([3, 2, 3, 1])
      True
      >>> [1, 2] == InAnyOrder([3, 2, 1])
      False
      >>> [{'a': 1}, {'b': 2}] == InAnyOrder([{'b': 2}, {'a': 1}])
      True
    """
    def __init__(self, values: Iterable[Any]):
        super().__init__()
        self.expected_values = values

    def _matches(self, other: Iterable[Any]) -> bool:
        values_left = [value for value in self.expected_values]
        for value in other:
            try:
                values_left.remove(value)
            except ValueError:
                return False
        return not values_left

    def _description(self) -> str:
        return repr(self.expected_values)


class SetEquals(Matcher):
    """A Matcher checking that an Iterable has the expected items, duplicates ignored.
    Faster than :class:`InAnyOrder` but less pedantic about duplicates and requires hashable items.

    The Iterable can be for example a list, tuple or set. Items must be hashable.

    :param values: An Iterable containing the expected items, in any order.

    Usage:
      >>> from pychoir import SetEquals
      >>> [1, 2, 3, 3] == SetEquals([3, 2, 1])
      True
      >>> [1, 2] == SetEquals([3, 2, 1])
      False
    """
    def __init__(self, values: Iterable[Any]):
        super().__init__()
        self.expected_values = values

    def _matches(self, other: Iterable[Any]) -> bool:
        return set(self.expected_values) == set(other)

    def _description(self) -> str:
        return repr(self.expected_values)


class _NotPresent:
    def __str__(self) -> str:
        return 'NotPresent'

    def __repr__(self) -> str:
        return str(self)


NotPresent = _NotPresent()


class IsNotPresentOr(Matcher):
    """A Matcher checking that a value is either :class:`NotPresent` or matches the passed matcher.
    Usually used for example with :class:`DictContainsAllOf`.

    :param matcher: The Mapping to find in the Mapping compared against.

    Usage:
      >>> from pychoir import DictContainsAllOf, IsNotPresentOr
      >>> {'a': 2} == DictContainsAllOf({'a': IsNotPresentOr(2)})
      True
      >>> {} == DictContainsAllOf({'a': IsNotPresentOr(2)})
      True
    """
    def __init__(self, matcher: Matchable):
        super().__init__()
        self.matcher = matcher

    def _matches(self, other: Any) -> bool:
        return other is NotPresent or self.nested_match(self.matcher, other)

    def _description(self) -> str:
        return repr(self.matcher)


class _First(Matcher):
    def __init__(self, how_many: int, matcher: Matchable):
        super().__init__()
        super()._override_name('First')
        self.how_many = how_many
        self.matcher = matcher

    def _matches(self, other: Sequence[Any]) -> bool:
        if self.how_many < 2:
            first = other[0]
        else:
            first = other[:self.how_many]
        return self.nested_match(self.matcher, first)

    def _description(self) -> str:
        matcher_string = repr(self.matcher)
        return f'{self.how_many})({matcher_string}'


class First(Transformer):
    """A Higher Order Matcher checking that the first `how_many` values match given matchers.
    The matcher is applied to the slice extracted from the passed :class:`Sequence`.

    :param how_many: The number of values to slice from the start of the sequence being compared.

    Usage:
      >>> from pychoir import First, All, GreaterThan
      >>> (1, 2, 3) == First(2)((1, 2))
      True
      >>> (1, 2, 3) == First()(1)
      True
    """
    def __init__(self, how_many: int = 1):
        super().__init__()
        self.how_many = how_many
        self.matcher: Optional[Matchable] = None

    def __call__(self, matcher: Matchable) -> _First:
        """
        :param matcher: The :class:`Matcher` to apply on the extracted slice.
        """
        return _First(self.how_many, matcher)


class _Last(Matcher):
    def __init__(self, how_many: int, matcher: Matchable):
        super().__init__()
        super()._override_name('Last')
        self.how_many = how_many
        self.matcher = matcher

    def _matches(self, other: Sequence[Any]) -> bool:
        if self.how_many < 2:
            last = other[-1]
        else:
            last = other[-self.how_many:]
        return self.nested_match(self.matcher, last)

    def _description(self) -> str:
        matcher_string = repr(self.matcher)
        return f'{self.how_many})({matcher_string}'


class Last(Transformer):
    """A Higher Order Matcher checking that the last `how_many` values match given matchers.
    The matcher is applied to the slice extracted from the passed :class:`Sequence`.

    :param how_many: The number of values to slice from the end of the sequence being compared.

    Usage:
      >>> from pychoir import Last, All, LessThan
      >>> (1, 2, 3) == Last(2)((2, 3))
      True
      >>> (1, 2, 3) == Last()(3)
      True
    """
    def __init__(self, how_many: int = 1):
        self.how_many = how_many

    def __call__(self, matcher: Matchable) -> _Last:
        """
        :param matcher: The :class:`Matcher` to apply on the extracted slice.
        """
        return _Last(self.how_many, matcher)


class _Slice(Matcher):
    def __init__(self, slice_: Union[int, slice], matcher: Matchable) -> None:
        super().__init__()
        super()._override_name(f'Slice[{slice_}]')
        self.slice = slice_
        self.matcher = matcher

    def _matches(self, other: Any) -> bool:
        sliced = other[self.slice]
        return self.nested_match(self.matcher, sliced)

    def _description(self) -> str:
        return repr(self.matcher)


class _SliceTransformer(Transformer):
    """Extracts `slice_` from the matched value before checking it with a Matcher.
    """
    def __init__(self, slice_: Union[int, slice]) -> None:
        self.slice: Union[int, slice] = slice_

    def __call__(self, matcher: Matchable) -> _Slice:
        """
        :param matcher: The :class:`Matcher` to apply on the extracted slice.
        """
        return _Slice(self.slice, matcher)


class _SliceFactory:
    """A Higher Order Matcher checking that the sliced values match given matchers.
    The matcher is applied to the slice extracted from the passed :class:`Sequence`.

    Usage:
      >>> from pychoir import Slice, And, IsInstance
      >>> (1, 2, 3) == Slice[1:3]((2, 3))
      True
      >>> (1, 2, 3) == Slice[2](And(IsInstance(int), 3))
      True
    """
    def __getitem__(self, slice_: Union[int, slice]) -> _SliceTransformer:
        """
        :param slice_: The :class:`slice` to slice from the matched object.
        """
        return _SliceTransformer(slice_)


Slice = _SliceFactory()
