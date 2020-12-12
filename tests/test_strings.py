from pychoir import EndsWith, StartsWith


def test_startswith():
    assert 'foobar' == StartsWith('foo')
    assert 'barbar' != StartsWith('foo')


def test_endswith():
    assert 'foobar' == EndsWith('bar')
    assert 'foo' != EndsWith('bar')
