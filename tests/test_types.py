from pychoir import IsInstance, OfType


def test_is_instance():
    assert OfType is IsInstance

    assert [1] == [IsInstance(int)]
    assert {'a': 'abc'} == {'a': IsInstance(str)}
    assert not ['abc'] == [IsInstance(int)]

    assert str([IsInstance(int)]) == '[IsInstance(int)]'
