from typing import Union

from .annotation import (
    SuccessResponse, ErrorResponse,
    ScalarInstantVector, ScalarRangeVector,
    VectorData, MatrixData, ScalarData, StringData,
)
from .model import (
    ScalarPoint, StringPoint,
    InstantSeries, RangeSeries,
    InstantVector, Matrix,
)


class PrometheusError(Exception):
    pass


class ParseError(Exception):
    pass


def parse_query_response(
    resp: Union[
        SuccessResponse[ScalarData],
        SuccessResponse[StringData],
        SuccessResponse[VectorData],
        ErrorResponse,
    ],
) -> Union[ScalarPoint, StringPoint, InstantVector]:
    if resp["status"] == "error":
        parse_error(resp)

    assert resp["status"] == "success", resp

    data = resp["data"]

    if data["resultType"] == "string":
        return parse_string(data)

    if data["resultType"] == "scalar":
        return parse_scalar(data)

    if data["resultType"] == "vector":
        return parse_vector(data)

    raise ParseError(f'unknown result type: {data["resultType"]}')


def parse_error(resp: ErrorResponse) -> None:
    raise PrometheusError(
        f'error {resp["errorType"]}: {resp["error"]}'
    )


def parse_instant_series(data: ScalarInstantVector) -> InstantSeries:
    return InstantSeries(
        metric=data["metric"],
        value=ScalarPoint(*data["value"])
    )


def parse_range_series(data: ScalarRangeVector) -> RangeSeries:
    return RangeSeries(
        metric=data["metric"],
        values=[
            ScalarPoint(*i)
            for i in data["values"]
        ]
    )


def parse_query_range_response(
    resp: Union[
        SuccessResponse[MatrixData],
        ErrorResponse,
    ],
) -> Matrix:
    if resp["status"] == "error":
        parse_error(resp)

    assert resp["status"] == "success", resp

    data = resp["data"]
    assert data["resultType"] == "matrix", resp

    return parse_matrix(data)


def parse_vector(data: VectorData) -> InstantVector:
    return InstantVector(series=[
        parse_instant_series(i)
        for i in data["result"]
    ])


def parse_matrix(data: MatrixData) -> Matrix:
    return Matrix(series=[
        parse_range_series(i)
        for i in data["result"]
    ])


def parse_scalar(data: ScalarData) -> ScalarPoint:
    return ScalarPoint(*data["result"])


def parse_string(data: StringData) -> StringPoint:
    return StringPoint(*data["result"])
