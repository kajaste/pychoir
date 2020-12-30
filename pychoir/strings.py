import re
import sys
from typing import Any, Union

from pychoir import Matcher

if sys.version_info >= (3, 7):
    from re import Pattern
else:
    Pattern = Any


class StartsWith(Matcher):
    """A Matcher checking that the compared string :code:`.startswith()` the passed string.

    :param start: The string the compared value is expected to start with.

    Usage:
      >>> from pychoir import StartsWith
      >>> 'foobar' == StartsWith('foo')
      True
      >>> 'barbar' == StartsWith('foo')
      False
    """
    def __init__(self, start: str):
        super().__init__()
        self.start = start

    def _matches(self, other: str) -> bool:
        return other.startswith(self.start)

    def _description(self) -> str:
        return repr(self.start)


class EndsWith(Matcher):
    """A Matcher checking that the compared string :code:`.endswith()` the passed string.

    :param end: The string the compared value is expected to end with.

    Usage:
      >>> from pychoir import EndsWith
      >>> 'foobar' == EndsWith('bar')
      True
      >>> 'foofoo' == EndsWith('bar')
      False
    """
    def __init__(self, end: str):
        super().__init__()
        self.end = end

    def _matches(self, other: str) -> bool:
        return other.endswith(self.end)

    def _description(self) -> str:
        return repr(self.end)


class MatchesRegex(Matcher):
    """A Matcher checking that the compared string matches the passed regular expression.

    :param regex: The regular expression (as a string or a :class:`re.Pattern`).

    Usage:
      >>> import re
      >>> from pychoir import MatchesRegex
      >>> 'foobar' == MatchesRegex(r'^f.obar')
      True
      >>> 'foofoo' == MatchesRegex(re.compile(r'^b[ao]r$'))
      False
    """
    def __init__(self, regex: Union[str, Pattern]):
        super().__init__()
        if isinstance(regex, str):
            regex = re.compile(regex)
        self.regex = regex

    def _matches(self, other: str) -> bool:
        return re.match(self.regex, other) is not None

    def _description(self) -> str:
        return repr(self.regex)
