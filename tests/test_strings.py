import re

from pychoir import EndsWith, StartsWith
from pychoir.strings import MatchesRegex


def test_startswith():
    assert 'foobar' == StartsWith('foo')
    assert 'barbar' != StartsWith('foo')

    assert str(StartsWith('foo')) == "StartsWith('foo')"


def test_endswith():
    assert 'foobar' == EndsWith('bar')
    assert 'foo' != EndsWith('bar')

    assert str(EndsWith('bar')) == "EndsWith('bar')"


def test_matches_regex():
    assert 'foobar' == MatchesRegex(r'^foo')
    assert 'foobar' == MatchesRegex(re.compile(r'^foo.ar$', flags=re.VERBOSE))
    assert 'bafoo' != MatchesRegex(r'^foo')

    assert str(MatchesRegex(re.compile(r'^foo', re.VERBOSE))) == "MatchesRegex(re.compile('^foo', re.VERBOSE))"
