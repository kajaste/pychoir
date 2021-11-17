from typing import Any, List

from pychoir.utils import i_removed, sequence_or_its_only_member


def test_sequence_or_its_first_member():
    empty_list: List[Any] = []
    assert sequence_or_its_only_member(empty_list) is empty_list
    assert sequence_or_its_only_member(['only']) == 'only'
    assert sequence_or_its_only_member(('several', 'members')) == ('several', 'members')


def test_i_removed():
    t = (0, 1, 2, 3, 4, 5)
    assert i_removed(t, 0) == (1, 2, 3, 4, 5)
    assert i_removed(t, 1) == (0, 2, 3, 4, 5)
    assert i_removed(t, 5) == (0, 1, 2, 3, 4)
    assert i_removed(t, 6) == t
