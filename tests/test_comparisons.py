from pychoir.comparisons import (
    EQ,
    GT,
    GTE,
    LT,
    LTE,
    NE,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
    LesserThan,
    LesserThanOrEqualTo,
    NotEqualTo,
)


def test_equal_to():
    assert EQ is EqualTo

    assert [1] == [EqualTo(1)]
    assert {'a': 1} == {'a': EqualTo(True)}
    assert not [0] == [EqualTo(1)]

    assert str(EqualTo(1)) == 'EqualTo(1)'


def test_not_equal_to():
    assert NE is NotEqualTo

    assert [0] == [NotEqualTo(1)]
    assert {'a': 0} == {'a': NotEqualTo(1)}
    assert not [0] == [NotEqualTo(0)]

    assert str(NotEqualTo(1)) == 'NotEqualTo(1)'


def test_greater_than():
    assert GT is GreaterThan

    assert [0] == [GreaterThan(-1)]
    assert {'a': 0} == {'a': GreaterThan(-1)}
    assert not [0] == [GreaterThan(0)]

    assert str(GreaterThan(-1)) == 'GreaterThan(-1)'


def test_greater_than_or_equal_to():
    assert GTE is GreaterThanOrEqualTo

    assert [0, 1] == [GreaterThanOrEqualTo(0), GreaterThanOrEqualTo(0)]
    assert {'a': 1} == {'a': GreaterThanOrEqualTo(1)}
    assert not [-1] == [GreaterThanOrEqualTo(0)]

    assert str(GreaterThanOrEqualTo(0)) == 'GreaterThanOrEqualTo(0)'


def test_lesser_than():
    assert LT is LesserThan

    assert [0] == [LesserThan(1)]
    assert {'a': 0} == {'a': LesserThan(1)}
    assert not [0] == [LesserThan(0)]

    assert str(LesserThan(2)) == 'LesserThan(2)'


def test_lesser_than_or_equal_to():
    assert LTE is LesserThanOrEqualTo

    assert [0, 1] == [LesserThanOrEqualTo(1), LesserThanOrEqualTo(1)]
    assert {'a': 0} == {'a': LesserThanOrEqualTo(0)}
    assert not [0] == [LesserThanOrEqualTo(-1)]

    assert str(LesserThanOrEqualTo(-1)) == 'LesserThanOrEqualTo(-1)'
