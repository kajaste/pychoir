# `pychoir` - Python Test Matchers for humans
[![PyPI version](http://img.shields.io/pypi/v/pychoir)](https://pypi.python.org/pypi/pychoir)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pychoir.svg)](https://pypi.python.org/pypi/pychoir/)
[![GitHub Actions (Tests)](https://github.com/kajaste/pychoir/workflows/Python%20package/badge.svg)](https://github.com/kajaste/pychoir)
[![Documentation Status](https://readthedocs.org/projects/pychoir/badge/?version=stable)](https://pychoir.readthedocs.io/en/stable/?badge=latest)
[![License](https://img.shields.io/pypi/l/pychoir.svg?style=flat)](https://github.com/kajaste/pychoir/blob/main/LICENSE.txt)

Super-duper low cognitive overhead matching for Python developers reading or writing tests. Implemented fully in modern & typed Python, without any dependencies. Runs and passes its tests on 3.6, 3.7, 3.8, 3.9 and 3.10. PyPy (3.6, 3.7) works fine too.

`pychoir` has mostly been developed for use with `pytest`, but nothing prevents from using it in any other test framework (like vanilla `unittest`) or even outside of testing, if you feel like it.

## Installation
* With pip: `pip install pychoir`
* With pipenv: `pipenv install --dev pychoir`
* With poetry: `poetry add --dev pychoir`

## Documentation
Check out the API Reference on readthedocs for detailed info and examples of all the available Matchers [https://pychoir.readthedocs.io/en/stable/api.html](https://pychoir.readthedocs.io/en/stable/api.html)

## Why?

You have probably written quite a few tests where you assert something like

```python
assert thing_under_test() == {'some_fields': 'some values'}
```

However, sometimes you do not expect _exact_ equivalence. So you start

```python
result = thing_under_test()

result_number = result.pop('number', None)
assert result_number is None or result_number < 3

result_list_of_strings = result.pop('list_of_strings', None)
assert (
    result_list_of_strings is not None
    and len(result_list_of_strings) == 5
    and all(isinstance(s, str) for s in result_list_of_strings)
)

assert result == {'some_fields': 'some values'}
```

...but this is not very convenient for anyone in the long run.

This is where `pychoir` comes in with matchers:

```python
from pychoir import LessThan, All, HasLength, IsNoneOr, IsInstance

assert thing_under_test() == {
    'number': IsNoneOr(LessThan(3)),
    'list_of_strings': HasLength(5) & All(IsInstance(str)),
    'some_fields': 'some values',
}
```

It can also be cumbersome to check mocked calls without using matchers:

```python
assert mock.call_args[0][0] < 3
assert isinstance(mock.call_args[0][1], str)
assert len(mock.call_args[0][2]) == 3
```

but simple and easy when using them:

```python
from pychoir import LessThan, IsInstance, HasLength

mock.assert_called_with(LessThan(3), IsInstance(str), HasLength(3))
```

You can also check many things about the same value: for example `IsInstance(int) & 5` will make sure that the value is not only equal to 5, but is also an `int` (goodbye to accidental `5.0`).

You can place a matcher almost anywhere where a value can be. **`pychoir` matchers work well inside lists, tuples, dicts, dataclasses, mock call assertions...** You can also place normal values inside matchers, and they will match as with traditional `==` or `!=`.

A core principle is that `pychoir` Matchers are composable and can be used freely in various combinations. For example `[LessThan(3) | 5]` is "equal to" a list with one item, holding a value equal to 5 or any value less than 3.

## Can I write custom Matchers of my own

Yes, you can! `pychoir` Matcher baseclass has been designed to be usable by code outside the library. It also takes care of most of the generic plumbing, so your custom matcher typically needs very little code.

Here is the implementation of `IsInstance` as an example:

```python
from typing import Any, Type
from pychoir import Matcher

class IsInstance(Matcher):
    def __init__(self, type_: Type[Any]):
        super().__init__()
        self.type = type_

    def _matches(self, other: Any) -> bool:
        return isinstance(other, self.type)

    def _description(self) -> str:
        return self.type.__name__

```

All you need to take care of is defining the parameters (if any) in `__init__()`, the match itself in `_matches()`, and a description of the parameters in `_description()`.

Here is an even simpler Anything matcher that does not take parameters and matches literally anything:

```python
from typing import Any
from pychoir import Matcher

class Anything(Matcher):
    def _matches(self, _: Any) -> bool:
        return True

    def _description(self) -> str:
        return ''
```

If your custom matcher is generic enough to be useful for everyone, please contribute (fork and make a pull request for now) and have it included in `pychoir`!

## Why not \<X\>?

### [PyHamcrest](https://github.com/hamcrest/PyHamcrest)

Nothing wrong with hamcrest as such, but `pychoir` aims to be better integrated with natural Python syntax, meaning for example that you do not need to use a custom assert function. `pychoir` matchers are drop-in replacements for your normal values alone or inside structures, even deeply nested ones. You can use hamcrest matchers through `pychoir` if you like, wrapping them in the `Matches(my_hamcrest_matcher)` matcher, although the idea is that `pychoir` would soon come with an equivalent set of matchers.

### [assertpy](https://github.com/assertpy/assertpy)

What a nice fluent API for matching, allowing matching multiple things at once. However, you can only match one value at a time. With `pychoir` you'll be matching the whole result at once, be it a single value, list, tuple, dict, dataclass, you name it. Let's see if `pychoir` gets some of that fluent stuff going forward as well.

### ???

I'd be happy to hear from you about other similar libraries.

## What is it based on?

Python has a rather peculiar way of handling equivalence, which allows customizing it in wild and imaginative ways. This is a very powerful feature, which one should usually avoid overusing. `pychoir` is built around the idea of using this power to build a lean and mean matcher implementation that looks like a custom DSL but is actually completely standard Python 3.

## What is the project status?

`pychoir` has quite a vast range of Matchers built in as well as basic API Reference documenting them. New ideas are still plenty and more can be discussed in [Discussions](https://github.com/kajaste/pychoir/discussions). Documentation will receive updates as well. Most remarkably fancy examples are missing. Making `pychoir` easier to contribute to is also on the list.

## Where does the name come from?

It comes from the French word _pochoir_ which means a [drawing technique](https://fr.wikipedia.org/wiki/Pochoir) using templates. For some reason this method of matching in tests reminds me of drawing with those. A French word was chosen because it happens to start with a p and a vowel ;)
