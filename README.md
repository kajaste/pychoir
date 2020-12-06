# PyChoir - Python Test Matchers for humans
[![PyPI version](https://badge.fury.io/py/pychoir.svg)](https://badge.fury.io/py/pychoir)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pychoir.svg)](https://pypi.python.org/pypi/pychoir/)
[![GitHub Actions (Tests)](https://github.com/Kajaste/pychoir/workflows/Python%20package/badge.svg)](https://github.com/kajaste/pychoir)

Super duper low cognitive overhead matching for Python developers reading or writing tests. Implemented in pure Python, without any dependencies. Runs and passes its tests on 3.6, 3.7, 3.8 and 3.9. PyPy (3.6, 3.7) works fine too.

PyChoir has mostly been developed for use with `pytest`, but nothing prevents from using it in any other test framework (like vanilla `unittest`) or even outside of testing, if you feel like it.

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

but this is not very convenient for anyone in the long run.

This is where PyChoir comes in with matchers:

```python
from pychoir import LessThan, All, HasLength, IsNoneOr, And, IsInstance

assert thing_under_test() == {
    'number': IsNoneOr(LessThan(3)),
    'list_of_strings': And(HasLength(5), All(IsInstance(str))),
    'some_fields': 'some values',
}
```

You can place a matcher almost anywhere where a value can be. **PyChoir matchers work well inside lists, tuples, dicts, dataclasses.** You can also place normal values inside matchers. A core principle is that PyChoir Matchers are composable and can be used freely in various combinations. For example `[Or(LessThan(3), 5)]` is "equal to" a list with one item, holding a value equal to 5 or any value less than 3.

## Can I write custom Matchers of my own

Yes, you can! PyChoir Matcher baseclass has been designed to be usable by code outside of the library. It also takes care of most of the generic plumbing, so your custom matcher typically needs very little code.

Here is the implementation of IsInstance as an example:

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

All you need to take care of is defining the parameters, the match itself, and a description of the parameters.

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

## Why not \<X\>?

### Hamcrest

Nothing wrong with hamcrest as such, but PyChoir aims to be better integrated with natural Python syntax. You can use hamcrest matchers through PyChoir if you like, wrapping them in the `Matches(my_hamcrest_matcher)` matcher.

### ???

I'd be happy to hear from you about other similar libraries.


## What is it based on?

Python has a rather peculiar way of handling equivalence, which allows customizing it in wild and imaginative ways. This is a very powerful feature, which one should usually avoid overusing. PyChoir is built around the idea of using this power to build a lean and mean matcher implementation that looks like a custom DSL but is actually completely standard Python 3.

## What is the project status?

This is only the very start. PyChoir is, however, already useful in many use cases and more features are coming. Next improvements are most likely going to be related to documentation.

## Where does the name come from?

It comes from the French word _pochoir_ which means a [drawing technique](https://fr.wikipedia.org/wiki/Pochoir) using templates. For some reason this method of matching in tests reminds me of drawing with those. A French word was chosen because it happens to start with a p and a vowel ;)
