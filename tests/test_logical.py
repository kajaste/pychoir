from contextlib import contextmanager
from typing import Iterator

from pychoir import (
    NE,
    AllOf,
    And,
    AnyOf,
    EqualTo,
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


def test_not_or():
    @contextmanager
    def make_not_or_123() -> Iterator[Not]:
        yield Not(Or(EqualTo(1), 2, 3))

    with make_not_or_123() as not_or_123:
        assert 4 == not_or_123
        assert str(not_or_123) == 'Not(Or(EqualTo(1), 2, 3))'

    with make_not_or_123() as not_or_123:
        assert not 4 != not_or_123
        assert str(not_or_123) == 'Not(Or(EqualTo(1)[FAILED for 4], 2, 3)[FAILED for 4])[FAILED for 4]'

    with make_not_or_123() as not_or_123:
        for i in (1, 2, 3):
            assert i != not_or_123
        assert str(not_or_123) == 'Not(Or(EqualTo(1), 2, 3))'

    with make_not_or_123() as not_or_123:
        for i in (1, 2, 3):
            assert not i == not_or_123
        assert str(not_or_123) == 'Not(Or(EqualTo(1)[FAILED for 1], 2, 3)[FAILED for (1, 2, 3)])[FAILED for (1, 2, 3)]'


def test_not_not():
    @contextmanager
    def make_not_one() -> Iterator[Not]:
        yield Not(1)

    with make_not_one() as not_one:
        assert 2 == not_one
        assert str(not_one) == 'Not(1)'

    with make_not_one() as not_one:
        assert 1 != not_one
        assert str(not_one) == 'Not(1)'

    with make_not_one() as not_one:
        assert not 2 != not_one
        assert str(not_one) == 'Not(1)[FAILED for 2]'

    with make_not_one() as not_one:
        assert not 1 == not_one
        assert str(not_one) == 'Not(1)[FAILED for 1]'

    @contextmanager
    def make_not_eq_one() -> Iterator[Not]:
        yield Not(EqualTo(1))

    with make_not_eq_one() as not_eq_one:
        assert 2 == not_eq_one
        assert str(not_eq_one) == 'Not(EqualTo(1))'

    with make_not_eq_one() as not_eq_one:
        assert 1 != not_eq_one
        assert str(not_eq_one) == 'Not(EqualTo(1))'

    with make_not_eq_one() as not_eq_one:
        assert not 2 != not_eq_one
        assert str(not_eq_one) == 'Not(EqualTo(1)[FAILED for 2])[FAILED for 2]'

    with make_not_eq_one() as not_eq_one:
        assert not 1 == not_eq_one
        assert str(not_eq_one) == 'Not(EqualTo(1)[FAILED for 1])[FAILED for 1]'

    @contextmanager
    def make_not_not_one() -> Iterator[Not]:
        yield Not(Not(1))

    with make_not_not_one() as not_not_one:
        assert 1 == not_not_one
        assert str(not_not_one) == 'Not(Not(1))'

    with make_not_not_one() as not_not_one:
        assert 2 != not_not_one
        assert str(not_not_one) == 'Not(Not(1))'

    with make_not_not_one() as not_not_one:
        assert not 1 != not_not_one
        assert str(not_not_one) == 'Not(Not(1)[FAILED for 1])[FAILED for 1]'

    with make_not_not_one() as not_not_one:
        assert not 2 == not_not_one
        assert str(not_not_one) == 'Not(Not(1)[FAILED for 2])[FAILED for 2]'

    @contextmanager
    def make_not_ne_one() -> Iterator[Not]:
        yield Not(NE(1))

    with make_not_ne_one() as not_ne_one:
        assert 1 == not_ne_one
        assert str(not_ne_one) == 'Not(NotEqualTo(1))'

    with make_not_ne_one() as not_ne_one:
        assert 2 != not_ne_one
        assert str(not_ne_one) == 'Not(NotEqualTo(1))'

    with make_not_ne_one() as not_ne_one:
        assert not 1 != not_ne_one
        assert str(not_ne_one) == 'Not(NotEqualTo(1)[FAILED for 1])[FAILED for 1]'

    with make_not_ne_one() as not_ne_one:
        assert not 2 == not_ne_one
        assert str(not_ne_one) == 'Not(NotEqualTo(1)[FAILED for 2])[FAILED for 2]'

    @contextmanager
    def make_not_not_eq_one() -> Iterator[Not]:
        yield Not(Not(EqualTo(1)))

    with make_not_not_eq_one() as not_not_eq_one:
        assert 1 == not_not_eq_one
        assert str(not_not_eq_one) == 'Not(Not(EqualTo(1)))'

    with make_not_not_eq_one() as not_not_eq_one:
        assert 2 != not_not_eq_one
        assert str(not_not_eq_one) == 'Not(Not(EqualTo(1)))'

    with make_not_not_eq_one() as not_not_eq_one:
        assert not 1 != not_not_eq_one
        assert str(not_not_eq_one) == 'Not(Not(EqualTo(1)[FAILED for 1])[FAILED for 1])[FAILED for 1]'

    with make_not_not_eq_one() as not_not_eq_one:
        assert not 2 == not_not_eq_one
        assert str(not_not_eq_one) == 'Not(Not(EqualTo(1)[FAILED for 2])[FAILED for 2])[FAILED for 2]'

    @contextmanager
    def make_not_not_eq_one_eq_two() -> Iterator[Not]:
        yield Not(Not(EqualTo(1), EqualTo(2)))

    with make_not_not_eq_one_eq_two() as not_not_eq_one_eq_two:
        assert 1 == not_not_eq_one_eq_two
        assert str(not_not_eq_one_eq_two) == 'Not(Not(EqualTo(1), EqualTo(2)))'

    with make_not_not_eq_one_eq_two() as not_not_eq_one_eq_two:
        assert not 2 != not_not_eq_one_eq_two
        assert (str(not_not_eq_one_eq_two)
                == 'Not(Not(EqualTo(1), EqualTo(2)[FAILED for 2])[FAILED for 2])[FAILED for 2]')

    with make_not_not_eq_one_eq_two() as not_not_eq_one_eq_two:
        assert not 1 != not_not_eq_one_eq_two
        assert (str(not_not_eq_one_eq_two)
                == 'Not(Not(EqualTo(1)[FAILED for 1], EqualTo(2))[FAILED for 1])[FAILED for 1]')

    with make_not_not_eq_one_eq_two() as not_not_eq_one_eq_two:
        assert 2 == not_not_eq_one_eq_two
        assert str(not_not_eq_one_eq_two) == 'Not(Not(EqualTo(1), EqualTo(2)))'


def test_results_true_for():
    assert {'a': 1} == {'a': ResultsTrueFor(bool)}
    assert ['foobar'] == [ResultsTrueFor(lambda x: x.startswith('foo'))]
    assert not {'a': 0} == {'a': ResultsTrueFor(bool)}

    assert str({'a': ResultsTrueFor(bool)}) == "{'a': ResultsTrueFor(<class 'bool'>)}"
