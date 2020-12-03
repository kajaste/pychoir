from pychoir import (
    All,
    Anything,
    EqualTo,
    In,
    Is,
    IsFalsy,
    IsNoneOr,
    IsTruthy,
    LessThan,
    Not,
    OneOf,
    Optionally,
)


def test_anything():
    assert [1] == [Anything()]
    assert [None] == [Anything()]
    assert [Ellipsis] == [Anything()]
    assert not [] == [Anything()]

    assert str(Anything()) == 'Anything()'


def test_is():
    assert [None] == [Is(None)]
    assert not [{}] == [Is({})]
    assert not [] == [Is(None)]

    assert str([Is(None)]) == '[Is(None)]'


def test_is_none_or():
    assert Optionally is IsNoneOr
    assert [None, 1] == All(Optionally(1))
    assert [None, 1] == [IsNoneOr(1), IsNoneOr(LessThan(0), EqualTo(1))]
    assert not [2] == [IsNoneOr(1)]

    assert str([IsNoneOr('1')]) == "[IsNoneOr('1')]"


def test_is_truthy():
    assert [1, True, [0], {0}, {'': None}, (0,)] == All(IsTruthy())
    assert [0, False, [], set(), {}, ()] == All(Not(IsTruthy()))

    assert str(All(Not(IsTruthy()))) == 'All(Not(IsTruthy()))'


def test_is_falsy():
    assert [0, False, [], set(), {}, ()] == All(IsFalsy())
    assert [1, True, [0], {0}, {'': None}, (0,)] == All(Not(IsFalsy()))

    assert str(All(Not(IsFalsy()))) == 'All(Not(IsFalsy()))'


def test_in():
    assert OneOf is In

    assert [1] == [In([1, 2])]
    assert 'a' == In({'a': 5})
    assert not [0] == [In([1, 2])]

    assert str([In(['1', '2'])]) == "[In(['1', '2'])]"
