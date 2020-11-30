from typing import Any

from pychoir.core import Matcher


class EqualTo(Matcher):
    def __init__(self, value: Any):
        self.value = value

    def matches(self, other: Any) -> bool:
        return bool(other == self.value)

    def description(self) -> str:
        return f'{self.value!r}'


EQ = EqualTo


class NotEqualTo(Matcher):
    def __init__(self, value: Any):
        self.value = value

    def matches(self, other: Any) -> bool:
        return bool(other != self.value)

    def description(self) -> str:
        return f'{self.value!r}'


NE = NotEqualTo


class GreaterThan(Matcher):
    def __init__(self, threshold: Any):
        self.threshold = threshold

    def matches(self, other: Any) -> bool:
        return bool(other > self.threshold)

    def description(self) -> str:
        return f'{self.threshold!r}'


GT = GreaterThan


class GreaterThanOrEqualTo(Matcher):
    def __init__(self, threshold: Any):
        self.threshold = threshold

    def matches(self, other: Any) -> bool:
        return bool(other >= self.threshold)

    def description(self) -> str:
        return f'{self.threshold!r}'


GTE = GreaterThanOrEqualTo


class LesserThan(Matcher):
    def __init__(self, threshold: Any):
        self.threshold = threshold

    def matches(self, other: Any) -> bool:
        return bool(other < self.threshold)

    def description(self) -> str:
        return f'{self.threshold!r}'


LT = LesserThan


class LesserThanOrEqualTo(Matcher):
    def __init__(self, threshold: Any):
        self.threshold = threshold

    def matches(self, other: Any) -> bool:
        return bool(other <= self.threshold)

    def description(self) -> str:
        return f'{self.threshold!r}'


LTE = LesserThanOrEqualTo
