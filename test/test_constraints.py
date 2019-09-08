import pytest

from ccc.util.constraints import process_constraint_string
from ccc.errors import ConstraintError


@pytest.mark.parametrize(
    "string,expected",
    [
        # name
        ("abcdefg", [[("abcdefg",)]]),
        # single comparisons
        ("red < 7", [[("lt", "red", 7)]]),
        ("red <= 7", [[("le", "red", 7)]]),
        ("red > 7", [[("gt", "red", 7)]]),
        ("red >= 7", [[("ge", "red", 7)]]),
        ("red == 7", [[("eq", "red", 7)]]),
        ("red != 7", [[("ne", "red", 7)]]),
        ("7 < red", [[("gt", "red", 7)]]),
        ("7 <= red", [[("ge", "red", 7)]]),
        ("7 > red", [[("lt", "red", 7)]]),
        ("7 >= red", [[("le", "red", 7)]]),
        ("7 == red", [[("eq", "red", 7)]]),
        ("7 != red", [[("ne", "red", 7)]]),
        # contains
        ("red in (7, 8, 9)", [[("in", "red", [7, 8, 9])]]),
        ("red not in (7, 8, 9)", [[("not_in", "red", [7, 8, 9])]]),
        # modulo
        ("red % 5 == 0", [[("mod", "red", 5, 0)]]),
        # chained comparisons
        ("3 < red < 7", [[("gt", "red", 3), ("lt", "red", 7)]]),
        ("3 < red <= 7", [[("gt", "red", 3), ("le", "red", 7)]]),
        # tuples of constraints
        ("3 < red, blue <= 9", [[("gt", "red", 3), ("le", "blue", 9)]]),
        ("3 < red, abcde, blue <= 9", [[("gt", "red", 3), ("abcde",), ("le", "blue", 9)]]),
        ("3 < red, abcde, blue <= 9", [[("gt", "red", 3), ("abcde",), ("le", "blue", 9)]]),
        ("abcde, 2 < blue <= 9", [[("abcde",), ("gt", "blue", 2), ("le", "blue", 9)]]),
        ("red in (7, 8, 9), xyz", [[("in", "red", [7, 8, 9]), ("xyz",)]]),
        # disjunctions
        ("red or blue", [[("red",)], [("blue",)]]),
        ("red or blue < 5", [[("red",)], [("lt", "blue", 5)]]),
        ("blue < 5 or red", [[("lt", "blue", 5)], [("red",)]]),
        ("red or (blue, yellow)", [[("red",)], [("blue",), ("yellow",)]]),
        ("(red, blue) or yellow", [[("red",), ("blue",)], [("yellow",)]]),
        (
            "a or (a, b) or (c < 5, b > 7, d)",
            [[("a",)], [("a",), ("b",)], [("lt", "c", 5), ("gt", "b", 7), ("d",)]],
        ),
    ],
)
def test_process_constraint_string_succeeds(string, expected):
    assert process_constraint_string(string) == expected


@pytest.mark.parametrize(
    "string",
    [
        "3331",
        "[]",
        "red < yellow",
        "red + yellow",
        "red + 5 == 32",
        "3 < red < 5 < 6",
        "red % 5 < 3",
        "red or (blue or yellow)",
    ],
)
def test_process_constraint_string_fails(string):
    with pytest.raises(ConstraintError):
        process_constraint_string(string)
