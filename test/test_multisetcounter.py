import itertools

import pytest

from ccc.multiset import Multiset


@pytest.mark.parametrize(
    "constraint,expected_degrees",
    [
        (("eq", "red", 5), {5}),
        (("ne", "red", 5), {0, 1, 2, 3, 4, 6, 7, 8, 9, 10}),
        (("lt", "red", 5), {0, 1, 2, 3, 4}),
        (("le", "red", 5), {0, 1, 2, 3, 4, 5}),
        (("gt", "red", 5), {6, 7, 8, 9, 10}),
        (("ge", "red", 5), {5, 6, 7, 8, 9, 10}),
        (("in", "red", [5, 8]), {5, 8}),
        (("not_in", "red", [5, 8]), {0, 1, 2, 3, 4, 6, 7, 9, 10}),
        (("mod", "red", 3, 1), {1, 4, 7, 10}),
    ],
)
def test_single_contraint(constraint, expected_degrees):
    """
    Test the constraint produces the correct set of integers.
    """
    ms = Multiset(10, constraints=[constraint])
    assert ms._degrees == {"red": expected_degrees}  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "constraint",
    [
        ("eq", "red", 5),
        ("ne", "red", 5),
        ("lt", "red", 5),
        ("le", "red", 5),
        ("gt", "red", 5),
        ("ge", "red", 5),
        ("in", "red", [5, 8]),
        ("not_in", "red", [5, 8]),
        ("mod", "red", 3, 1),
    ],
)
def test_constraint_application_is_idemptotent(constraint):
    """
    Test applying the same constraint again has no effect.
    """
    ms_1 = Multiset(10, constraints=[constraint])
    ms_2 = Multiset(10, constraints=[constraint] * 2)
    assert ms_1._degrees == ms_2._degrees  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "constraints,expected_degrees",
    [
        ([("lt", "red", 5), ("lt", "red", 4), ("lt", "red", 3)], {0, 1, 2}),
        ([("le", "red", 5), ("le", "red", 4), ("le", "red", 3)], {0, 1, 2, 3}),
        ([("le", "red", 5), ("ge", "red", 1), ("ne", "red", 3)], {1, 2, 4, 5}),
        ([("ne", "red", 5), ("ne", "red", 1), ("ne", "red", 3)], {0, 2, 4, 6, 7, 8, 9, 10}),
        ([("eq", "red", 5), ("eq", "red", 1), ("eq", "red", 3)], set()),
        ([("mod", "red", 3, 1), ("lt", "red", 7)], {1, 4}),
        ([("in", "red", (5, 6, 7)), ("in", "red", (4, 8))], set()),
        ([("in", "red", (5, 6, 7)), ("in", "red", (6, 8))], {6}),
        ([("in", "red", (5, 6, 7)), ("not_in", "red", (6, 8))], {5, 7}),
        ([("not_in", "red", (5, 6, 7)), ("not_in", "red", (0, 6, 8))], {1, 2, 3, 4, 9, 10}),
        ([("mod", "red", 2, 0), ("mod", "red", 4, 0)], {0, 4, 8}),
    ],
)
def test_multiple_constraints(constraints, expected_degrees):
    """
    Test applying multiple constraints produces the correct result,
    and any permutation of these constraints produces this result.
    """
    for constraint_perm in itertools.permutations(constraints):
        ms = Multiset(10, constraints=constraint_perm)
        assert ms._degrees == {"red": expected_degrees}  # pylint: disable=protected-access


def test_no_constraints_with_collection():
    """
    Test the correct set of integers in generated when
    passing a collection but no constraints.
    """
    ms = Multiset(10, constraints=None, collection={"red": 3, "blue": 2})
    assert ms._degrees == {  # pylint: disable=protected-access
        "red": {0, 1, 2, 3},
        "blue": {0, 1, 2},
    }


@pytest.mark.parametrize(
    "constraint,expected_degrees",
    [
        (("eq", "red", 5), {5}),
        (("lt", "red", 5), {0, 1, 2, 3, 4}),
        (("ge", "red", 5), {5, 6, 7, 8}),
    ],
)
def test_single_contraint_with_collection(constraint, expected_degrees):
    """
    Test the constraint produces the correct set of integers
    when a collection is also specified.
    """
    ms = Multiset(8, constraints=[constraint], collection={"red": 8, "blue": 2})
    assert ms._degrees["red"] == expected_degrees  # pylint: disable=protected-access
    assert ms._degrees["blue"] == {0, 1, 2}  # pylint: disable=protected-access
