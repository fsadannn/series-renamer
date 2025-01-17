import datetime
from abc import abstractmethod
from math import floor
from operator import le
from re import Match
from typing import (
    Callable,
    Container,
    Generic,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar('T')

_current_year = datetime.date.today().year
_year_gap = 100


def is_valid_year(txt: str) -> bool:
    txt = txt.strip()
    try:
        data = int(txt)

        if 1920 <= data <= _current_year + _year_gap:
            return True

        return False
    except ValueError:
        return False


def number_to_str(number: Union[float, int]) -> str:
    has_fraction = abs(number - floor(number)) > 1e-9

    if has_fraction:
        return str(number)

    return str(int(number))


class Stack:  # pragma: no cover
    __slots__ = ('_stack', '_id')

    def __init__(self, idd: str = ''):
        self._stack: list = []
        self._id = idd

    def __len__(self):
        return len(self._stack)

    @property
    def id(self) -> str:
        return self._id

    @property
    def stack(self) -> list:
        return self._stack

    @property
    def empty(self) -> bool:
        return len(self._stack) == 0

    def isempty(self) -> bool:
        return len(self._stack) == 0

    def top(self):
        if len(self._stack) == 0:
            raise IndexError('top from empty Stack')
        return self._stack[-1]

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if len(self._stack) == 0:
            raise IndexError('pop from empty Stack')
        val = self._stack.pop()
        return val

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}< id="{self.id}" >'


class GContainer(Generic[T], Container):
    __slots__ = ('_comparison_fn',)

    def __init__(self, comparison_fn: Callable[[T], bool]):
        self._comparison_fn = comparison_fn

    def __contains__(self, obj: T) -> bool:
        return self._comparison_fn(obj)


class MatchP(Protocol):
    @abstractmethod
    def group(self, *args: Union[int, str]) -> Union[str, Tuple[str]]:
        raise NotImplementedError

    @abstractmethod
    def groups(self, *args: Union[int, str]) -> Tuple[str]:
        raise NotImplementedError


class TMatch(MatchP):
    __slots__ = ('_text',)

    def __init__(self, text: str):
        self._text = text

    def group(self, *args: Union[int, str]) -> Union[str, Tuple[str]]:
        if len(args) != 0:
            raise IndexError

        return self._text

    def groups(self, *args: Union[int, str]) -> Tuple[str]:
        if len(args) != 0:
            raise IndexError

        return (self._text,)


class PatternP(Protocol):
    @abstractmethod
    def match(self, string: str, *args) -> Optional[MatchP]:
        raise NotImplementedError

    @abstractmethod
    def search(self, string: str, *args) -> Optional[MatchP]:
        raise NotImplementedError


class TPattern(PatternP):
    __slots__ = ('_comparison_fn',)

    def __init__(self, comparison_fn: Callable[[T], bool]):
        self._comparison_fn = comparison_fn

    def __find(self, string: str) -> Optional[MatchP]:
        if not self._comparison_fn(string):
            return None

        return TMatch(string)

    def match(self, string: str, *args) -> Optional[MatchP]:
        return self.__find(string)

    def search(self, string: str, *args) -> Optional[MatchP]:
        return self.__find(string)
