from typing import Any

from pychoir.callables import WhenPassedTo


def test_returns() -> None:
    assert "5" == WhenPassedTo(int).returns(5)
    assert "5" != WhenPassedTo(int).returns(6)

    assert str(WhenPassedTo(int).returns(5)) == 'WhenPassedTo(int).returns(5)'


def test_raises() -> None:
    def raiser(_: Any) -> None:
        raise RuntimeError('raiser raised')

    assert "lol" == WhenPassedTo(raiser).raises()
    assert "lol" == WhenPassedTo(int).raises(ValueError)
    assert 5 != WhenPassedTo(int).raises()

    assert str(WhenPassedTo(raiser).raises(ValueError)) == 'WhenPassedTo(raiser).raises(ValueError)'


def test_does_not_raise() -> None:
    def raiser(_: Any) -> None:
        raise RuntimeError('raiser raised')

    assert "5" == WhenPassedTo(int).does_not_raise()
    assert "lol" != WhenPassedTo(int).does_not_raise()
    assert not Any == WhenPassedTo(raiser).does_not_raise()

    assert str(WhenPassedTo(raiser).does_not_raise()) == 'WhenPassedTo(raiser).does_not_raise()'
