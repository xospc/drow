from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")
Converter = Callable[[str], T]


def no_op(value: T) -> T:
    return value
