from typing import Union, TypeVar
from collections.abc import Callable

from .annotation import (
    SuccessResponse, ErrorResponse,
    ScalarInstantVector, ScalarRangeVector,
    ScalarPointData,
    VectorData, MatrixData, ScalarData, StringData,
)
from .model import (
    ScalarPoint, StringPoint,
    InstantSeries, RangeSeries,
    InstantVector, Matrix,
)
from .converter import Converter

T = TypeVar("T")
ValueType = TypeVar("ValueType")
ResponseType = TypeVar("ResponseType")
ResultType = TypeVar("ResultType")

QueryResponse = Union[
    SuccessResponse[ScalarData],
    SuccessResponse[StringData],
    SuccessResponse[VectorData],
    ErrorResponse,
]
type QueryResult[T] = Union[
    ScalarPoint[T], StringPoint, InstantVector[T],
]
QueryRangeResponse = Union[
    SuccessResponse[MatrixData],
    ErrorResponse,
]
QueryRangeResult = Matrix


class PrometheusError(Exception):
    pass


class ParseError(Exception):
    pass


def generic_parse_query_response(
    resp: QueryResponse,
    value_converter: Converter[T],
) -> QueryResult[T]:
    if resp["status"] == "error":
        parse_error(resp)

    assert resp["status"] == "success", resp

    data = resp["data"]

    if data["resultType"] == "string":
        return parse_string(data)

    if data["resultType"] == "scalar":
        return parse_scalar(data, value_converter=value_converter)

    if data["resultType"] == "vector":
        return parse_vector(data, value_converter=value_converter)

    raise ParseError(f'unknown result type: {data["resultType"]}')


def parse_error(resp: ErrorResponse) -> None:
    raise PrometheusError(
        f'error {resp["errorType"]}: {resp["error"]}'
    )


def parse_instant_series(
    data: ScalarInstantVector,
    value_converter: Converter[T],
) -> InstantSeries[T]:
    return InstantSeries(
        metric=data["metric"],
        # value=ScalarPoint(*data["value"])
        value=parse_scalar_point(
            data["value"], value_converter=value_converter,
        ),
    )


def parse_range_series(
    data: ScalarRangeVector,
    value_converter: Converter[T]
) -> RangeSeries[T]:
    return RangeSeries(
        metric=data["metric"],
        values=[
            # ScalarPoint(*i)
            parse_scalar_point(i, value_converter=value_converter)
            for i in data["values"]
        ]
    )


def generic_parse_query_range_response(
    resp: QueryRangeResponse,
    value_converter: Converter[T],
) -> QueryRangeResult[T]:
    if resp["status"] == "error":
        parse_error(resp)

    assert resp["status"] == "success", resp

    data = resp["data"]
    assert data["resultType"] == "matrix", resp

    return parse_matrix(data, value_converter=value_converter)


def parse_vector(
    data: VectorData,
    value_converter: Converter[T],
) -> InstantVector[T]:
    return InstantVector(series=[
        parse_instant_series(i, value_converter=value_converter)
        for i in data["result"]
    ])


def parse_matrix(data: MatrixData, value_converter: Converter[T]) -> Matrix[T]:
    return Matrix(series=[
        parse_range_series(i, value_converter=value_converter)
        for i in data["result"]
    ])


def parse_scalar(
    data: ScalarData, value_converter: Converter[T],
) -> ScalarPoint[T]:
    return parse_scalar_point(data["result"], value_converter)


def parse_scalar_point(
    data: ScalarPointData,
    value_converter: Converter[T],
) -> ScalarPoint[T]:
    t, v = data
    return ScalarPoint(t, value_converter(v))


def parse_string(data: StringData) -> StringPoint:
    return StringPoint(*data["result"])


def generic_parse_query_value_response(
    resp: QueryResponse,
    value_converter: Converter[T],
) -> T:
    if resp["status"] == "error":
        parse_error(resp)

    assert resp["status"] == "success", resp

    data = resp["data"]

    if data["resultType"] == "string":
        return value_converter(data["result"][1])

    if data["resultType"] == "scalar":
        return value_converter(data["result"][1])

    if data["resultType"] == "vector":
        series_count = len(data["result"])
        if series_count != 1:
            raise ParseError(f"series count incorrect: {series_count}")

        return value_converter(data["result"][0]["value"][1])

    raise ParseError(f'unknown result type: {data["resultType"]}')


def make_parser(
    origin_parser: Callable[
        [ResponseType, Converter[ValueType]],
        ResultType
    ],
    value_converter: Converter[ValueType],
) -> Callable[[ResponseType], ResultType]:
    def parser(resp: ResponseType) -> ResultType:
        return origin_parser(resp, value_converter)

    return parser
