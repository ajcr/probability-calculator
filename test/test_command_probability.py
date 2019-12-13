import pytest

from ccc.commands.probability import draw_command, permutation_command


@pytest.mark.parametrize(
    "size,constraints,collection,expected",
    [
        # https://math.stackexchange.com/questions/898683
        (8, "r>=1,b>=1,g>=1,w>=1,bl>=1,gr>=1", "r=5;b=5;g=5;w=5;bl=5;gr=5", "5000/26013"),
        # https://math.stackexchange.com/questions/897730
        (6, "r >= 1, g >= 1", "r=10; g=10", "639/646"),
        # https://math.stackexchange.com/questions/2979053
        (4, "(r==2, w==2) or (r==2, b==2) or (b==2, w==2)", "w=25;r=2;b=3", "401/9135"),
        # https://math.stackexchange.com/questions/334516
        (3, "r==3 or g==3 or b==3", "r=3; g=4; b=5", "3/44"),
        # https://math.stackexchange.com/questions/2419834
        (4, "blue == 0", "red = 3; blue = 1; yellow = 2", "1/3"),
    ],
)
def test_count_draws_no_replacement(runner, size, constraints, collection, expected):
    result = runner.invoke(
        draw_command, ["--number", size, "--constraints", constraints, "--from", collection]
    )
    assert result.output.rstrip() == expected


@pytest.mark.parametrize(
    "size,constraints,collection,expected",
    [
        # https://math.stackexchange.com/questions/529254/probability-of-draw-with-replacement
        (3, "red == 2, blue == 1", "red = 4; blue = 6", "36/125"),
        # https://math.stackexchange.com/questions/2100892/probability-with-replacement-at-least-scenario
        (4, "red >= 2", "red = 1; green = 5", "19/144"),
        # https://math.stackexchange.com/questions/1540823/probabilty-of-drawing-atleast-1-red-ball-in-3-attempts
        (3, "red >= 1", "red = 5; blue = 5; green = 5", "19/27"),
        # https://math.stackexchange.com/questions/2419834
        (4, "blue == 0", "red = 3; blue = 1; yellow = 2", "625/1296"),
    ],
)
def test_count_draws_with_replacement(runner, size, constraints, collection, expected):
    result = runner.invoke(
        draw_command,
        ["--number", size, "--constraints", constraints, "--from", collection, "--replace"],
    )
    assert result.output.rstrip() == expected


@pytest.mark.parametrize(
    "sequence,constraints,expected",
    [("food", "no_adjacent", "1/2"), ("food", "derangement", "1/6")],
)
def test_count_permutations(runner, sequence, constraints, expected):
    result = runner.invoke(permutation_command, [sequence, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize(
    "sequence,expected,expected_if_same_distinct",
    [
        ("a", "1", "1"),
        ("aa", "0", "0"),
        ("aab", "1/3", "1/3"),
        ("aabb", "1/3", "1/3"),
        ("food", "1/2", "1/2"),
    ],
)
def test_probability_permutations_no_adjacent(
    runner, sequence, expected, expected_if_same_distinct
):
    result = runner.invoke(permutation_command, [sequence, "--constraints", "no_adjacent"])
    assert result.output.rstrip() == str(expected)
    result = runner.invoke(
        permutation_command, [sequence, "--constraints", "no_adjacent", "--same-distinct"]
    )
    assert result.output.rstrip() == str(expected_if_same_distinct)


@pytest.mark.parametrize(
    "sequence,expected,expected_if_same_distinct",
    [
        ("a", 0, 0),
        ("ab", "1/2", "1/2"),
        ("abb", 0, 0),
        ("aabb", "1/6", "1/6"),
        ("aaabb", 0, 0),
        ("abbc", "1/6", "1/6"),
    ],
)
def test_count_permutations_derangement(runner, sequence, expected, expected_if_same_distinct):
    result = runner.invoke(permutation_command, [sequence, "--constraints", "derangement"])
    assert result.output.rstrip() == str(expected)
    result = runner.invoke(
        permutation_command, [sequence, "--constraints", "derangement", "--same-distinct"]
    )
    assert result.output.rstrip() == str(expected_if_same_distinct)
