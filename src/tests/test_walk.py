from unittest.mock import Mock, call

from walk import walk
import pytest


def test_walk_dict_keys():
    d = {"b": 1, "c": 2}

    mock = Mock()
    walk(d, mock)
    assert mock.call_count == 2
    mock.assert_has_calls([call("b", 1), call("c", 2)])


def test_array_keys():
    d = {"arr": [1, 2, 3]}
    mock = Mock()
    walk(d, mock)
    assert mock.call_count == 3
    mock.assert_has_calls([call("arr.[0]", 1), call("arr.[1]", 2), call("arr.[2]", 3)])


def test_walking_dict_nested_path():
    d = {"a": {"b": 1, "c": 2}}

    mock = Mock()
    walk(d, mock)
    assert mock.call_count == 2
    mock.assert_has_calls([call("a.b", 1), call("a.c", 2)])


# noinspection PyTypeChecker
def test_apply_typemissmatch():
    with pytest.raises(AssertionError):
        walk(1, lambda p, c: c)

    class MyList(list):
        pass

    try:
        walk(MyList(), lambda p, c: c)
    except AssertionError:
        raise AssertionError("Should work for list ancestors")

    class MyDict(dict):
        pass

    try:
        walk(MyDict(), lambda p, c: c)
    except AssertionError:
        raise AssertionError("Should work for list ancestors")
