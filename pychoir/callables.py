from typing import Any, Callable, Optional, Type

from pychoir import Matcher


class WhenPassedTo:
    """Matchers that check how a value behaves when passed to a callable.

    :param callable_: The callable to pass the value to.

    Usage:
      >>> from pychoir import WhenPassedTo
      >>> "foo" == WhenPassedTo(int).raises(ValueError)
      True
      >>> "5" == WhenPassedTo(int).does_not_raise()
      True
      >>> "5" == WhenPassedTo(int).returns(5)
      True
    """
    def __init__(self, callable_: Callable[[Any], Any]):
        self.callable = callable_

    def returns(self, value: Any) -> Matcher:
        return _Returns(self.callable, value)

    def raises(self, exception: Optional[Type[Exception]] = None) -> Matcher:
        return _Raises(self.callable, exception)

    def does_not_raise(self) -> Matcher:
        return _DoesNotRaise(self.callable)


class _Returns(Matcher):
    def __init__(self, callable_: Callable[[Any], Any], value: Any):
        super().__init__(name='WhenPassedTo')
        self.callable = callable_
        self.value = value

    def _matches(self, other: Any) -> bool:
        return bool(self.callable(other) == self.value)

    def _description(self) -> str:
        callable_name = _name_or_repr(self.callable)

        return f'{callable_name}).returns({self.value!r}'


class _Raises(Matcher):
    def __init__(self, callable_: Callable[..., Any], exception: Optional[Type[Exception]]):
        super().__init__(name='WhenPassedTo')
        self.callable = callable_
        self.exception = exception

    def _matches(self, other: Any) -> bool:
        raised = None
        try:
            self.callable(other)
        except Exception as e:
            raised = e
        if self.exception is not None:
            return isinstance(raised, self.exception)
        else:
            return raised is not None

    def _description(self) -> str:
        callable_name = _name_or_repr(self.callable)
        exception_name = _name_or_repr(self.exception)

        return f'{callable_name}).raises({exception_name}'


class _DoesNotRaise(Matcher):
    def __init__(self, callable_: Callable[..., Any]):
        super().__init__(name='WhenPassedTo')
        self.callable = callable_

    def _matches(self, other: Any) -> bool:
        try:
            self.callable(other)
        except Exception:
            return False
        return True

    def _description(self) -> str:
        callable_name = _name_or_repr(self.callable)
        return f'{callable_name}).does_not_raise('


def _name_or_repr(thing: Any) -> str:
    return getattr(thing, '__name__', None) or repr(thing)
