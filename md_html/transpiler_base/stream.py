import collections
import io
from typing import Generic, Iterable, TypeVar, Iterator
import itertools


T = TypeVar("T", bound=io.StringIO)


class EmptyStream(BaseException):
    ...


class Stream(Generic[T]):
    _iterator: Iterator[T]

    def __init__(self, iterable__: Iterable[T]):
        self._iterator = iter(iterable__)
        self._current = EmptyStream

    def next(self) -> T:
        self._current = next(self._iterator)
        return self._current

    @property
    def current(self) -> T:
        if self._current is not EmptyStream:
            return self._current
        raise ValueError('iterator did\'nt start')