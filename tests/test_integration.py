from typing import Any, Optional, TypeVar

from pychoir import M, Matches

T = TypeVar('T')


def test_hamcrest() -> None:
    class Description:
        pass

    class TestHamcrestLike:
        def __init__(self, return_value: bool):
            self.return_value = return_value

        def matches(self, item: T, mismatch_description: Optional[Description] = None) -> bool:
            return self.return_value

    matching_matcher = TestHamcrestLike(True)
    mismatching_matcher = TestHamcrestLike(False)

    assert ['a'] == [Matches(matching_matcher)]
    assert not ['a'] == [M(mismatching_matcher)]

    assert (str(Matches(TestHamcrestLike(True)))
            .startswith('Matches(<tests.test_integration.test_hamcrest.<locals>.TestHamcrestLike object at'))


def test_matches() -> None:
    assert M is Matches

    class TestMatcherLike:
        def __init__(self, return_value: bool):
            self.return_value = return_value

        def matches(self, _: Any) -> bool:
            return self.return_value

    matching_matcher = TestMatcherLike(True)
    mismatching_matcher = TestMatcherLike(False)

    assert ['a'] == [Matches(matching_matcher)]
    assert not ['a'] == [Matches(mismatching_matcher)]
