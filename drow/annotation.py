from typing import TypeVar, TypedDict, NotRequired, Generic, Literal, TypeAlias

DataType = TypeVar("DataType")
PointData: TypeAlias = tuple[float, DataType]


class BaseResponse(TypedDict):
    warnings: NotRequired[list[str]]
    infos: NotRequired[list[str]]


class SuccessResponse(BaseResponse, Generic[DataType]):
    status: Literal["success"]
    data: DataType


class ErrorResponse(BaseResponse):
    status: Literal["error"]
    errorType: str
    error: str


# 0: int: boundary_rule
# 1: str: left_boundary
# 2: str: right_boundary
# 3: str: count_in_bucket
BucketValue = tuple[int, str, str, str]


class HistogramValue(TypedDict):
    count: str
    sum: str
    buckets: list[BucketValue]


class BaseVector(TypedDict):
    metric: dict[str, str]


class ScalarInstantVector(BaseVector):
    value: PointData[str]


class HistogramInstantVector(BaseVector):
    histogram: PointData[HistogramValue]


class ScalarRangeVector(BaseVector):
    values: list[PointData[str]]


class HistogramRangeVector(BaseVector):
    histograms: list[PointData[HistogramValue]]


class VectorData(TypedDict):
    resultType: Literal["vector"]
    result: list[ScalarInstantVector]


class MatrixData(TypedDict):
    resultType: Literal["matrix"]
    result: list[ScalarRangeVector]


class ScalarData(TypedDict):
    resultType: Literal["scalar"]
    result: PointData[str]


class StringData(TypedDict):
    resultType: Literal["string"]
    result: PointData[str]
