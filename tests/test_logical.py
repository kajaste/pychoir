from pychoir import (
    AllOf,
    And,
    AnyOf,
    GreaterThan,
    HasLength,
    IsInstance,
    IsNoneOf,
    Not,
    Or,
    ResultsTrueFor,
)


def test_and():
    assert AllOf is And

    assert [1] == [And(IsInstance(int), GreaterThan(0))]
    assert {'a': [1]} == {'a': And(IsInstance(list), HasLength(GreaterThan(0)))}
    assert not {'a': []} == {'a': And(IsInstance(list), HasLength(GreaterThan(0)))}

    assert str(And(IsInstance(list), HasLength(GreaterThan(0)))) == 'And(IsInstance(list), HasLength(GreaterThan(0)))'


def test_or():
    assert AnyOf is Or

    assert [1] == [Or(0, 1)]
    assert {'a': [1]} == {'a': [Or(0, 1, 2)]}
    assert not [2] == [Or(0, 1)]

    assert str([Or(0, 1)]) == '[Or(0, 1)]'


def test_not():
    assert IsNoneOf is Not

    assert [1] == [IsNoneOf(0, 2, GreaterThan(3))]
    assert {'a': [None]} == {'a': IsNoneOf(Ellipsis, 0, [])}
    assert not [1] == [IsNoneOf(0, 1, 2)]

    assert str([Not(0, 1, 2)]) == '[Not(0, 1, 2)]'


def test_results_true_for():
    assert {'a': 1} == {'a': ResultsTrueFor(bool)}
    assert ['foobar'] == [ResultsTrueFor(lambda x: x.startswith('foo'))]
    assert not {'a': 0} == {'a': ResultsTrueFor(bool)}

    assert str({'a': ResultsTrueFor(bool)}) == "{'a': ResultsTrueFor(<class 'bool'>)}"
