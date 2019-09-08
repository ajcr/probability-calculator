import pytest

from ccc.util.collection import process_collection_string


@pytest.mark.parametrize(
    "string,expected", [("red = 7", {"red": 7}), ("red = 7; blue = 9", {"red": 7, "blue": 9})]
)
def test_process_collection_string_succeeds(string, expected):
    assert process_collection_string(string) == expected
