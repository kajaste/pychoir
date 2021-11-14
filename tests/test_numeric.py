from pychoir import IsEven, IsNegative, IsNonNegative, IsOdd, IsPositive


def test_is_even():
    assert 0 == IsEven()
    assert -2 == IsEven()
    assert 2 == IsEven()
    assert 1 != IsEven()

    assert str(IsEven()) == 'IsEven()'


def test_is_odd():
    assert 1 == IsOdd()
    assert -1 == IsOdd()
    assert 0 != IsOdd()
    assert -2 != IsOdd()

    assert str(IsOdd()) == 'IsOdd()'


def test_is_positive():
    assert 1 == IsPositive()
    assert 2 == IsPositive()
    assert 0 != IsPositive()
    assert -1 != IsPositive()

    assert str(IsPositive()) == 'IsPositive()'


def test_is_non_negative():
    assert 1 == IsNonNegative()
    assert 0 == IsNonNegative()
    assert -1 != IsNonNegative()

    assert str(IsNonNegative()) == 'IsNonNegative()'


def test_is_negative():
    assert -1 == IsNegative()
    assert 0 != IsNegative()
    assert 1 != IsNegative()

    assert str(IsNegative()) == 'IsNegative()'
