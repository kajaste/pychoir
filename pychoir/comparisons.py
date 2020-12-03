from typing import Any

from pychoir.core import Matcher


class EqualTo(Matcher):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return bool(other == self.value)

    def _description(self) -> str:
        return repr(self.value)


EQ = EqualTo


class NotEqualTo(Matcher):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def _matches(self, other: Any) -> bool:
        return bool(other != self.value)

    def _description(self) -> str:
        return repr(self.value)


NE = NotEqualTo


class GreaterThan(Matcher):
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other > self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


GT = GreaterThan


class GreaterThanOrEqualTo(Matcher):
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other >= self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


GTE = GreaterThanOrEqualTo


class LessThan(Matcher):
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other < self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


LT = LessThan


class LessThanOrEqualTo(Matcher):
    def __init__(self, threshold: Any):
        super().__init__()
        self.threshold = threshold

    def _matches(self, other: Any) -> bool:
        return bool(other <= self.threshold)

    def _description(self) -> str:
        return repr(self.threshold)


LTE = LessThanOrEqualTo
