from typing import Any

from pychoir import Matcher


class IsOdd(Matcher):
    """A Matcher checking that the value compared against it is odd.

    Usage:
      >>> from pychoir import IsOdd
      >>> 5 == IsOdd()
      True
      >>> 4 == IsOdd()
      False
    """
    def _matches(self, other: Any) -> bool:
        return bool(other % 2 == 1)

    def _description(self) -> str:
        return ''


class IsEven(Matcher):
    """A Matcher checking that the value compared against it is even.

    Usage:
      >>> from pychoir import IsEven
      >>> 4 == IsEven()
      True
      >>> 5 == IsEven()
      False
    """
    def _matches(self, other: Any) -> bool:
        return bool(other % 2 == 0)

    def _description(self) -> str:
        return ''


class IsPositive(Matcher):
    """A Matcher checking that the value compared against it is positive.

    Usage:
      >>> from pychoir import IsPositive
      >>> 1 == IsPositive()
      True
      >>> 0 == IsPositive()
      False
    """
    def _matches(self, other: Any) -> bool:
        return bool(other > 0)

    def _description(self) -> str:
        return ''


class IsNonNegative(Matcher):
    """A Matcher checking that the value compared against it is non-negative.

    Usage:
      >>> from pychoir import IsPositive
      >>> 1 == IsNonNegative()
      True
      >>> 0 == IsNonNegative()
      True
      >>> -1 == IsNonNegative()
      False
    """
    def _matches(self, other: Any) -> bool:
        return bool(other >= 0)

    def _description(self) -> str:
        return ''


class IsNegative(Matcher):
    """A Matcher checking that the value compared against it is negative.

    Usage:
      >>> from pychoir import IsNegative
      >>> -1 == IsNegative()
      True
      >>> 0 == IsNegative()
      False
    """
    def _matches(self, other: Any) -> bool:
        return bool(other < 0)

    def _description(self) -> str:
        return ''
