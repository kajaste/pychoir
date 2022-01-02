import sys
from contextlib import contextmanager
from typing import Any, Dict, List, cast
from unittest.mock import MagicMock

import pytest

from pychoir import (
    And,
    Anything,
    EqualTo,
    GreaterThan,
    InAnyOrder,
    IsInstance,
    IsOdd,
    IsTruthy,
    Matchable,
    Matcher,
    that,
)


def test_matchable():
    def matcher(matchable: Matchable) -> bool:
        return matchable == 5

    assert matcher(5) is True


class TestMatcher:
    class _TestMatcher(Matcher):
        def __init__(self, does_match: bool):
            super().__init__(name='Matcher')
            self.does_match = does_match

        def _matches(self, other: Any) -> bool:
            return self.does_match

        def _description(self) -> str:
            return f'{self.does_match}'

    def test_as(self):
        instance = self._TestMatcher(True)
        assert instance.as_(int) is cast(int, instance)
        assert type(instance.as_(int)) is cast(int, self._TestMatcher)
        assert instance.as_(int) == 5

    def test_eq(self):
        assert self._TestMatcher(True) == 1
        assert 0 == self._TestMatcher(True)
        assert not self._TestMatcher(False) == 0
        assert not 0 == self._TestMatcher(False)

    def test_ne(self):
        assert 0 != self._TestMatcher(False)

    def test_str(self):
        assert str(self._TestMatcher(True)) == 'Matcher(True)'

    def test_repr(self):
        assert repr(self._TestMatcher(True)) == 'Matcher(True)'

    def test_failure_report(self):
        with pytest.raises(AssertionError) as exc_info:
            assert 'foo' == self._TestMatcher(False)
        assert "Matcher(False)[FAILED for 'foo']" in str(exc_info.value)

    def test_failure_report_on_mismatch_outside_matcher(self):
        with pytest.raises(AssertionError) as exc_info:
            matching_matcher = self._TestMatcher(True)
            assert {'a': 1, 'b': 0} == {'a': matching_matcher, 'b': 1}
        assert "assert {'a': 1, 'b': 0} == {'a': Matcher(True), 'b': 1}" in str(exc_info.value)
        assert str(matching_matcher) == 'Matcher(True)'

    def test_nested_match(self):
        @contextmanager
        def new_matching_matcher():
            yield self._TestMatcher(True)
        with new_matching_matcher() as matching_matcher:
            assert str(matching_matcher) == 'Matcher(True)'
        with new_matching_matcher() as matching_matcher:
            assert Anything().nested_match(matching_matcher, 1)
            assert str(matching_matcher) == 'Matcher(True)'
        with new_matching_matcher() as matching_matcher:
            assert Anything().nested_match(matching_matcher, 1, expect_mismatch=True)
            assert str(matching_matcher) == 'Matcher(True)[FAILED for 1]'
            assert Anything().nested_match(matching_matcher, 2, expect_mismatch=True)
            assert str(matching_matcher) == 'Matcher(True)[FAILED for (1, 2)]'

        @contextmanager
        def new_mismatching_matcher():
            yield self._TestMatcher(False)
        with new_mismatching_matcher() as mismatching_matcher:
            assert str(mismatching_matcher) == 'Matcher(False)'
        with new_mismatching_matcher() as mismatching_matcher:
            assert not Anything().nested_match(mismatching_matcher, 3, expect_mismatch=True)
            assert str(mismatching_matcher) == 'Matcher(False)'
        with new_mismatching_matcher() as mismatching_matcher:
            assert not Anything().nested_match(mismatching_matcher, 3)
            assert str(mismatching_matcher) == 'Matcher(False)[FAILED for 3]'
            assert not Anything().nested_match(mismatching_matcher, 4)
            assert str(mismatching_matcher) == 'Matcher(False)[FAILED for (3, 4)]'

        assert Anything().nested_match(1, 1)
        assert Anything().nested_match(1, 1, expect_mismatch=True)
        assert not Anything().nested_match(1, 2)
        assert not Anything().nested_match(1, 2, expect_mismatch=True)

    def test_and_operator(self) -> None:
        assert 5 == IsInstance(int) & 5
        assert 5 != EqualTo(5) & IsInstance(float)

        assert str(EqualTo(5) & IsInstance(int)) == '(EqualTo(5) & IsInstance(int))'

        failing_and_operator = EqualTo(5) & IsInstance(float)
        assert not 5 == failing_and_operator
        assert str(failing_and_operator) == '(EqualTo(5) & IsInstance(float)[FAILED for 5])[FAILED for 5]'

        one_and = EqualTo(5) & IsInstance(int)
        another_and = IsOdd() & IsTruthy()
        combo_and = one_and & another_and
        assert 5 == combo_and
        assert 6 != combo_and
        assert str(combo_and) == '(EqualTo(5) & IsInstance(int) & IsOdd() & IsTruthy())'

        and_and_normal = one_and & IsTruthy()
        assert 5 == and_and_normal
        assert str(and_and_normal) == '(EqualTo(5) & IsInstance(int) & IsTruthy())'

    def test_or_operator(self) -> None:
        assert 5 == IsInstance(float) | 5
        assert 5 != EqualTo(6) | IsInstance(float)

        assert str(EqualTo(5) | IsInstance(int)) == '(EqualTo(5) | IsInstance(int))'

        failing_or_operator = EqualTo(5) | IsInstance(float)
        assert not 6 == failing_or_operator
        assert str(failing_or_operator) == '(EqualTo(5)[FAILED for 6] | IsInstance(float)[FAILED for 6])[FAILED for 6]'

        one_or = EqualTo(5) | IsInstance(int)
        another_or = IsOdd() | IsTruthy()
        combo_or = one_or | another_or
        assert 5 == combo_or
        assert 6 == combo_or
        assert str(combo_or) == '(EqualTo(5) | IsInstance(int) | IsOdd() | IsTruthy())'

        or_or_normal = one_or | IsTruthy()
        assert 6 == or_or_normal
        assert str(or_or_normal) == '(EqualTo(5) | IsInstance(int) | IsTruthy())'


def test_matcher_in_mock_call_params():
    m = MagicMock()

    m(5)
    m.assert_called_once_with(Anything())
    m.assert_called_once_with(And(IsInstance(int), GreaterThan(3)))

    with pytest.raises(AssertionError) as exc_info:
        m.assert_called_once_with(GreaterThan(5))
    if sys.version_info >= (3, 8):
        assert (str(exc_info.value)
                == "expected call not found.\n"
                   "Expected: mock(GreaterThan(5)[FAILED for 5])\n"
                   "Actual: mock(5)")
    else:
        assert (str(exc_info.value)
                == "Expected call: mock(GreaterThan(5)[FAILED for 5])\n"
                   "Actual call: mock(5)")

    m.do_stuff_to([{'a': 1}, {'a': 2}])
    m.do_stuff_to.assert_called_once_with(InAnyOrder([{'a': 2}, {'a': 1}]))


def test_assert_that_matches():
    assert that(5).matches(And(EqualTo(5), IsInstance(int)))

    with pytest.raises(AssertionError) as exc_info:
        assert that(5).matches(EqualTo(4))
    assert str(exc_info.value).split('\n')[0] == 'assert that(5).matches(EqualTo(4)[FAILED for 5])'


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
