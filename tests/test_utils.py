from typing import Any, List

from pychoir.utils import sequence_or_its_only_member


def test_sequence_or_its_first_member():
    empty_list: List[Any] = []
    assert sequence_or_its_only_member(empty_list) is empty_list
    assert sequence_or_its_only_member(['only']) == 'only'
    assert sequence_or_its_only_member(('several', 'members')) == ('several', 'members')
