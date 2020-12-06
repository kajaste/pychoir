import sys
from typing import Any, Dict, List, cast
from unittest.mock import MagicMock, patch

import pytest

from pychoir import Anything, IsInstance, IsTruthy, Matchable, Matcher


def test_matchable():
    def matcher(matchable: Matchable) -> bool:
        return matchable == 5

    assert matcher(5) is True


class TestMatcher:
    class _TestMatcher(Matcher):
        def __init__(self, does_match: bool):
            super().__init__()
            self.does_match = does_match

        def _matches(self, other: Any) -> bool:
            return self.does_match

        def _description(self) -> str:
            return f'does_match={self.does_match}'

    def test_as(self):
        instance = self._TestMatcher(True)
        assert instance.as_(int) is cast(int, instance)
        assert type(instance.as_(int)) is self._TestMatcher
        assert instance.as_(int) == 5

    def test_eq(self):
        assert self._TestMatcher(True) == 1
        assert 0 == self._TestMatcher(True)
        assert not self._TestMatcher(False) == 0
        assert not 0 == self._TestMatcher(False)

    def test_ne(self):
        assert 0 != self._TestMatcher(False)

    def test_str(self):
        assert str(self._TestMatcher(True)) == '_TestMatcher(does_match=True)'

    def test_repr(self):
        assert repr(self._TestMatcher(True)) == '_TestMatcher(does_match=True)'

    def test_failure_report(self):
        with pytest.raises(AssertionError) as excinfo:
            assert 'foo' == self._TestMatcher(False)
        assert "_TestMatcher(does_match=False)[FAILED for 'foo']" in str(excinfo.value)

    def test_nested_match(self):
        matching_matcher = self._TestMatcher(True)
        assert str(matching_matcher) == '_TestMatcher(does_match=True)'
        assert Anything().nested_match(matching_matcher, 1)
        assert str(matching_matcher) == '_TestMatcher(does_match=True)'
        assert not Anything().nested_match(matching_matcher, 1, inverse=True)
        assert str(matching_matcher) == '_TestMatcher(does_match=True)[FAILED for 1]'
        assert not Anything().nested_match(matching_matcher, 2, inverse=True)
        assert str(matching_matcher) == '_TestMatcher(does_match=True)[FAILED for (1, 2)]'

        mismatching_matcher = self._TestMatcher(False)
        assert str(mismatching_matcher) == '_TestMatcher(does_match=False)'
        assert Anything().nested_match(mismatching_matcher, 3, inverse=True)
        assert str(mismatching_matcher) == '_TestMatcher(does_match=False)'
        assert not Anything().nested_match(mismatching_matcher, 3)
        assert str(mismatching_matcher) == '_TestMatcher(does_match=False)[FAILED for 3]'
        assert not Anything().nested_match(mismatching_matcher, 4)
        assert str(mismatching_matcher) == '_TestMatcher(does_match=False)[FAILED for (3, 4)]'

        assert Anything().nested_match(1, 1)
        assert not Anything().nested_match(1, 1, inverse=True)
        assert not Anything().nested_match(1, 2)
        assert Anything().nested_match(1, 2, inverse=True)

    @patch('warnings.warn')
    def test_warn_when_reusing(self, warn_mock: MagicMock) -> None:
        instance = self._TestMatcher(True)
        assert instance == 1
        warn_mock.assert_not_called()
        assert instance == 2
        warn_mock.assert_called_once_with(
            'Erroneous re-run of _TestMatcher(does_match=True). Create a new Matcher instance for each use!'
        )

    @patch('warnings.warn')
    def test_nested_match_allows_reuse(self, warn_mock: MagicMock) -> None:
        instance = self._TestMatcher(True)
        assert Anything().nested_match(instance, 1)
        warn_mock.assert_not_called()
        assert Anything().nested_match(instance, 2)
        warn_mock.assert_not_called()


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
