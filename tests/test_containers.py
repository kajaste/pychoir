from pychoir.comparisons import LTE, GreaterThan
from pychoir.containers import (
    All,
    AreNot,
    ContainsAllOf,
    ContainsAnyOf,
    ContainsNoneOf,
    DictContainsAllOf,
    HasLength,
    Len,
)
from pychoir.logical import And
from pychoir.types import IsInstance


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
    dict_to_match = {'a': And(HasLength(3), All(IsInstance(int))), 'b': 4}
    assert not test_input == dict_to_match
    assert test_input == DictContainsAllOf(dict_to_match)

    assert not test_input == DictContainsAllOf({'a': [1]})
    assert not test_input == DictContainsAllOf({'a': [1, 2, 3], 'b': 4, 'c': 'extra', 'd': 'not there'})

    assert (str(DictContainsAllOf({'a': And(HasLength(3), All(IsInstance(int))), 'b': 4}))
            == "DictContainsAllOf({'a': And(HasLength(3), All(IsInstance(int))), 'b': 4})")
