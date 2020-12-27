from typing import Any

from pychoir.core import Matcher


class EqualTo(Matcher):
    """A somewhat redundant matcher checking for equality. Most Matchers can take
    values and/or Matchers and **you should prefer bare values instead of wrapping them
    in EqualTo**.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import EqualTo
      >>> 1 == EqualTo(1)
      True
    """
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return bool(other == self.value)

    def _description(self) -> str:
        return repr(self.value)


EQ = EqualTo


class NotEqualTo(Matcher):
    """A Matcher checking that compared value is not equal to the given value.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import NotEqualTo
      >>> 1 == NotEqualTo(2)
      True
      >>> 1 == NotEqualTo(1)
      False
    """
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return bool(other != self.value)

    def _description(self) -> str:
        return repr(self.value)


NE = NotEqualTo


class GreaterThan(Matcher):
    """A Matcher checking that compared value is greater than the given value.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import GreaterThan
      >>> [2] == [GreaterThan(2)]
      False
      >>> 3 == GreaterThan(2)
      True
    """
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other > self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


GT = GreaterThan


class GreaterThanOrEqualTo(Matcher):
    """A Matcher checking that compared value is greater than or equal to the given value.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import GreaterThanOrEqualTo
      >>> 2 == GreaterThanOrEqualTo(2)
      True
      >>> 1 == GreaterThanOrEqualTo(2)
      False
    """
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other >= self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


GTE = GreaterThanOrEqualTo


class LessThan(Matcher):
    """A Matcher checking that compared value is less than the given value.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import LessThan
      >>> 2 == LessThan(2)
      False
      >>> 1 == LessThan(2)
      True
    """
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other < self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


LT = LessThan


class LessThanOrEqualTo(Matcher):
    """A Matcher checking that compared value is less than or equal to the given value.

    :param value: The value to compare against.

    Usage:
      >>> from pychoir import LessThanOrEqualTo
      >>> 2 == LessThanOrEqualTo(2)
      True
      >>> 3 == LessThanOrEqualTo(2)
      False
    """
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other <= self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


LTE = LessThanOrEqualTo
