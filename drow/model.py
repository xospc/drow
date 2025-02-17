from dataclasses import dataclass


@dataclass(frozen=True)
class ScalarPoint:
    timestamp: float
    value: str


@dataclass(frozen=True)
class StringPoint:
    timestamp: float
    value: str


@dataclass(frozen=True)
class InstantSeries:
    metric: dict[str, str]
    value: ScalarPoint


@dataclass(frozen=True)
class InstantVector:
    series: list[InstantSeries]


@dataclass(frozen=True)
class RangeSeries:
    metric: dict[str, str]
    values: list[ScalarPoint]


@dataclass(frozen=True)
class Matrix:
    series: list[RangeSeries]
