import sys
from typing import Any, Dict, List

import pytest

from pychoir.core import Matchable, Matcher
from pychoir.existential import IsTruthy
from pychoir.types import IsInstance


def test_matchable():
    def matcher(matchable: Matchable) -> bool:
        return matchable == 5

    assert matcher(5) is True


def test_matcher():
    class TestMatcher(Matcher):
        def __init__(self, does_match: bool):
            self.does_match = does_match

        def matches(self, other: Any) -> bool:
            return self.does_match

        def description(self) -> str:
            return f'does_match={self.does_match}'

    true_matcher = TestMatcher(True)
    false_matcher = TestMatcher(False)

    assert true_matcher == 1
    assert 0 == true_matcher
    assert not false_matcher == 0
    assert not 0 == false_matcher
    assert 0 != false_matcher

    assert str(true_matcher) == 'TestMatcher(does_match=True)'

    with pytest.raises(AssertionError) as excinfo:
        assert 'foo' == false_matcher
    assert str(excinfo.value) == "assert 'foo' == TestMatcher(does_match=False)"


if sys.version_info >= (3, 7):
    from dataclasses import dataclass

    def test_matcher_in_dataclass():
        @dataclass
        class Data:
            i: int
            ldsb: List[Dict[str, bool]]

        assert Data(1, [{'foo': True}]) == Data(IsInstance(int).as_(int), [{'foo': IsTruthy().as_(bool)}])

        assert (str(Data(IsInstance(int).as_(int), [{'foo': IsTruthy().as_(bool)}]))
                == "test_matcher_in_dataclass.<locals>.Data(i=IsInstance(int), ldsb=[{'foo': IsTruthy()}])")
