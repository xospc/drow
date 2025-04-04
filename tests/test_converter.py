from decimal import Decimal
from unittest import TestCase

from drow.annotation import SuccessResponse, VectorData
from drow.model import InstantVector
from drow.parser import generic_parse_query_response
from drow.converter import convert_to_decimal


class TestConverter(TestCase):
    def test_convert_to_decimal(self) -> None:
        resp: SuccessResponse[VectorData] = {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {
                            "job": "foo",
                        },
                        "value": (1435781451.781, "1.23456789"),
                    },
                ],
            },
        }
        parsed = generic_parse_query_response(resp, convert_to_decimal)
        assert isinstance(parsed, InstantVector)
        value = parsed.series[0].value.value

        assert isinstance(value, Decimal)
        self.assertEqual(value, Decimal("1.23456789"))
