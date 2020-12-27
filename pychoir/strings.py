import re
import sys
from typing import Any, Union

from pychoir import Matcher

if sys.version_info >= (3, 7):
    from re import Pattern
else:
    Pattern = Any


class StartsWith(Matcher):
    def __init__(self, start: str):
        super().__init__()
        self.start = start

    def _matches(self, other: str) -> bool:
        return other.startswith(self.start)

    def _description(self) -> str:
        return repr(self.start)


class EndsWith(Matcher):
    def __init__(self, end: str):
        super().__init__()
        self.end = end

    def _matches(self, other: str) -> bool:
        return other.endswith(self.end)

    def _description(self) -> str:
        return repr(self.end)


class MatchesRegex(Matcher):
    def __init__(self, regex: Union[str, Pattern]):
        super().__init__()
        if isinstance(regex, str):
            regex = re.compile(regex)
        self.regex = regex

    def _matches(self, other: str) -> bool:
        return re.match(self.regex, other) is not None

    def _description(self) -> str:
        return repr(self.regex)
