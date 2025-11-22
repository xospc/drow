from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass(frozen=True)
class Point(Generic[T]):
    timestamp: float
    value: T


@dataclass(frozen=True)
class InstantSeries(Generic[T]):
    metric: dict[str, str]
    value: Point[T]


@dataclass(frozen=True)
class InstantVector(Generic[T]):
    series: list[InstantSeries[T]]


@dataclass(frozen=True)
class RangeSeries(Generic[T]):
    metric: dict[str, str]
    values: list[Point[T]]


@dataclass(frozen=True)
class Matrix(Generic[T]):
    series: list[RangeSeries[T]]
