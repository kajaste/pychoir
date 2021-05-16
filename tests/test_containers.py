from typing import Any, Dict

import pytest

from pychoir import (
    LTE,
    All,
    And,
    AreNot,
    ContainsAllOf,
    ContainsAnyOf,
    ContainsNoneOf,
    DictContainsAllOf,
    EqualTo,
    First,
    GreaterThan,
    HasLength,
    InAnyOrder,
    IsEmpty,
    IsInstance,
    IsNotPresentOr,
    Last,
    Len,
    LessThan,
    Matcher,
    NotPresent,
    SetEquals,
    Slice,
)


def test_is_empty():
    assert {'a': []} == {'a': IsEmpty()}
    assert ['foo', '', 'bar'] == ['foo', IsEmpty(), 'bar']
    assert not 'foo' == IsEmpty()

    assert str(IsEmpty()) == 'IsEmpty()'


def test_has_length():
    assert Len is HasLength

    assert {'a': [1, 2, 3]} == {'a': HasLength(3)}
    assert ['123'] == [HasLength(LTE(3))]
    assert not ['1'] == [HasLength(3)]

    assert str(HasLength(1)) == 'HasLength(1)'


def test_all():
    assert {'a': [1, 2, 3]} == {'a': All(IsInstance(int), GreaterThan(0))}
    assert not [-1, 1, 2, 3] == All(GreaterThan(0))

    assert str(All(GreaterThan(0))) == 'All(GreaterThan(0))'


def test_are_not():
    assert [1, 2, 3] == AreNot(IsInstance(str))
    assert not [1, 2, ''] == AreNot(IsInstance(str))

    assert str(AreNot(IsInstance(str))) == 'AreNot(IsInstance(str))'


def test_contains_all_of():
    assert {'a': [1, 2, 3]} == {'a': ContainsAllOf(3, 2, 1)}
    assert not ['12'] == [ContainsAllOf('1', '2', '3')]

    assert str([ContainsAllOf('1', '2', '3')]) == "[ContainsAllOf('1', '2', '3')]"


def test_contains_any_of():
    assert {'a': [1, 2, 3]} == {'a': ContainsAnyOf(5, 3, 1)}
    assert not ['12'] == [ContainsAnyOf('5', '3')]

    assert str([ContainsAnyOf('5', '3')]) == "[ContainsAnyOf('5', '3')]"


def test_contains_none_of():
    assert {'a': [1, 2, 3]} == {'a': ContainsNoneOf(4, 5, 6)}
    assert not ['123'] == [ContainsNoneOf('5', '3', '1')]

    assert str([ContainsNoneOf('5', '3', '1')]) == "[ContainsNoneOf('5', '3', '1')]"


def test_dict_contains_all_of():
    test_input = {'a': [1, 2, 3], 'b': 4, 'c': 'extra'}

    def dict_to_match() -> Dict[Any, Any]:
        return {'a': And(HasLength(3), All(IsInstance(int))), 'b': 4, 'd': NotPresent}

    assert not test_input == dict_to_match()
    assert test_input == DictContainsAllOf(dict_to_match())

    assert not test_input == DictContainsAllOf({'a': [1]})
    assert not test_input == DictContainsAllOf({'a': [1, 2, 3], 'b': 4, 'c': 'extra', 'e': 'not there'})

    assert (str(DictContainsAllOf({'a': And(HasLength(3), All(IsInstance(int))), 'b': 4, 'd': NotPresent}))
            == "DictContainsAllOf({'a': And(HasLength(3), All(IsInstance(int))), 'b': 4, 'd': NotPresent})")


def test_in_any_order():
    assert [1, 2, 3] == InAnyOrder([3, 2, 1])
    assert [1, 2, 3] != InAnyOrder([3, 2])
    assert [1, 2, 3] != InAnyOrder([3, 2, 1, 0])
    assert [1, 2, 2] == InAnyOrder([2, 1, 2])
    assert [1, 2, 2] != InAnyOrder([1, 1, 2])

    assert {1, 2, 3} == InAnyOrder({3, 2, 1})
    assert {1, 2, 3} == InAnyOrder((3, 2, 1))
    assert [{'a': 1}, {'b': 2}] == InAnyOrder([{'b': 2}, {'a': 1}])

    assert str(InAnyOrder([1, 2, 3])) == 'InAnyOrder([1, 2, 3])'


def test_set_equals():
    assert [1, 2, 3] == SetEquals([3, 2, 1])
    assert [1, 2, 3] != SetEquals([3, 2])
    assert [1, 2, 3] != SetEquals([3, 2, 1, 0])
    assert [1, 2, 2] == SetEquals([2, 1, 2])
    assert [1, 2, 2] == SetEquals([1, 1, 2])

    assert {1, 2, 3} == SetEquals({3, 2, 1})
    assert {1, 2, 3} == SetEquals((3, 2, 1))

    assert str(SetEquals([1, 2, 3])) == 'SetEquals([1, 2, 3])'


def test_is_not_present_or():
    with_a = {'a': 1, 'b': 2, 'c': 'whatever'}
    without_a = {'b': 2, 'c': 'whatever'}

    def matcher() -> Matcher:
        return DictContainsAllOf({'a': IsNotPresentOr(1), 'b': 2})

    assert with_a == matcher()
    assert without_a == matcher()

    assert {'a': 2, 'b': 2} != matcher()
    assert {'b': 1} != matcher()

    assert str(matcher()) == "DictContainsAllOf({'a': IsNotPresentOr(1), 'b': 2})"


def test_first():
    assert 'abcdef' == First(3)('abc')
    assert [1, 2, 3, 'a', 'b', 'c'] == First(3)(All(IsInstance(int)))
    assert [1, 2, 3, 'a', 'b', 'c'] != First(4)(All(IsInstance(int)))
    assert [1, 2, 3] == First()(1)

    with pytest.raises(AssertionError):
        assert [1, 2, 3] == First(2)

    with pytest.raises(TypeError) as te_info:
        assert [1, 2, 3] == First(2)([0, 1])([2])  # type: ignore
    assert str(te_info.value).split('\n')[0] == "'_First' object is not callable"

    with pytest.raises(AssertionError) as exc_info:
        assert [1, 2, 3] == First(2)([0, 1])
    assert str(exc_info.value).split('\n')[0] == 'assert [1, 2, 3] == First(2)([0, 1])[FAILED for [1, 2, 3]]'


def test_last():
    assert 'abcdef' == Last(3)('def')
    assert [1, 2, 3, 'a', 'b', 'c'] == Last(3)(All(IsInstance(str)))
    assert [1, 2, 3, 'a', 'b', 'c'] != Last(4)(All(IsInstance(str)))
    assert [1, 2, 3] == Last()(3)

    with pytest.raises(AssertionError):
        assert [1, 2, 3] == Last(2)

    with pytest.raises(TypeError) as te_info:
        assert [1, 2, 3] == Last(2)([0, 1])([2])  # type: ignore
    assert str(te_info.value) == "'_Last' object is not callable"

    with pytest.raises(AssertionError) as exc_info:
        assert [1, 2, 3] == Last(2)([1, 2])
    assert str(exc_info.value).split('\n')[0] == 'assert [1, 2, 3] == Last(2)([1, 2])[FAILED for [1, 2, 3]]'


def test_slice():
    assert 'abcdef' == Slice[3:](EqualTo('def'))
    assert 'abcdef' == Slice[:3](All(LessThan('d')))
    assert [1, 2, 3] == Slice[1](EqualTo(2))

    with pytest.raises(AssertionError):
        assert [1, 2, 3] == Slice[2]

    with pytest.raises(TypeError) as te_info:
        assert [1, 2, 3] == Slice[2:3]([0, 1])([2])  # type: ignore
    assert str(te_info.value) == "'_Slice' object is not callable"

    with pytest.raises(AssertionError) as exc_info:
        assert [1, 2, 3] == Slice[0](EqualTo(0))
    assert (
        str(exc_info.value).split('\n')[0] ==
        'assert [1, 2, 3] == Slice[0](EqualTo(0)[FAILED for 1])[FAILED for [1, 2, 3]]'
    )
