import pytest

from ccc.commands.count import multisets, sequences, permutations, draws


@pytest.mark.parametrize(
    "size,constraints,expected",
    [
        # https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/
        # 6-042j-mathematics-for-computer-science-fall-2005/readings/ln11.pdf
        (6, "apple % 2 == 0, orange <= 4, pear in (0, 1), banana % 5 == 0", 7),
        (100, "apple % 2 == 0, orange <= 4, pear in (0, 1), banana % 5 == 0", 101),
        # https://projecteuler.net/problem=31
        (200, "a%1==0, b%2==0, c%5==0, d%10==0, e%20==0, f%50==0, g%100==0, h%200==0", 73682),
    ],
)
def test_count_multisets(runner, size, constraints, expected):
    result = runner.invoke(multisets, ["--size", size, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize(
    "size,constraints,expected",
    [
        (4, "f == 1, o == 2, d == 1", 12),
        # https://math.stackexchange.com/questions/960046
        (3, "a <= 2, b <= 3", 7),
        (3, "m <= 1, p <= 2, i <= 4, s <= 4", 53),
    ],
)
def test_count_sequences(runner, size, constraints, expected):
    result = runner.invoke(sequences, ["--size", size, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize(
    "sequence,expected,expected_if_same_distinct",
    [("a", 1, 1), ("aa", 1, 2), ("ab", 2, 2), ("food", 12, 24), ("abc", 6, 6)],
)
def test_count_permutations_no_constraints(runner, sequence, expected, expected_if_same_distinct):
    result = runner.invoke(permutations, [sequence])
    assert result.output.rstrip() == str(expected)
    result = runner.invoke(permutations, [sequence, "--same-distinct"])
    assert result.output.rstrip() == str(expected_if_same_distinct)


@pytest.mark.parametrize(
    "size,collection,constraints,expected",
    [
        (4, "blue = 12; red = 16; green = 11", "red <= 3 or blue == 3", 80431),
        (5, "blue = 12; red = 16; green = 11", "red <= 3 or blue == 3", 529529),
        (5, "blue = 12; red = 16; green = 11", "(blue == 1, red <= 3) or blue == 3", 265980),
        (
            5,
            "blue = 12; red = 16; green = 11",
            "(blue == 1, red <= 3) or blue == 3 or green == 2",
            354860,
        ),
        (
            5,
            "blue = 12; red = 16; green = 11",
            "(blue == 1, red <= 3) or blue == 3 or green >= 2",
            391292,
        ),
        (5, "blue = 5; red = 16; green = 11", "blue == 5 or blue == 0", 80731),
    ],
)
def test_count_draws(runner, size, collection, constraints, expected):
    result = runner.invoke(
        draws, ["--size", size, "--collection", collection, "--constraints", constraints]
    )
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize(
    "sequence,expected,expected_if_same_distinct",
    [
        ("a", 1, 1),
        ("aa", 0, 0),
        ("aab", 1, 2),
        ("aabb", 2, 8),
        ("food", 6, 12),
        ("mississippi", 2016, 2322432),
        # https://www.quora.com/In-how-many-cases-there-will-be-no-two-people-of-the-same-nationality-sitting-next-to-each-other
        ("aaabbbccc", 174, 37584),
    ],
)
def test_count_permutations_no_adjacent(runner, sequence, expected, expected_if_same_distinct):
    result = runner.invoke(permutations, [sequence, "--constraints", "no_adjacent"])
    assert result.output.rstrip() == str(expected)
    result = runner.invoke(
        permutations, [sequence, "--constraints", "no_adjacent", "--same-distinct"]
    )
    assert result.output.rstrip() == str(expected_if_same_distinct)


@pytest.mark.parametrize(
    "sequence,expected,expected_if_same_distinct",
    [
        ("a", 0, 0),
        ("ab", 1, 1),
        ("abb", 0, 0),
        ("aabb", 1, 4),
        ("aaabb", 0, 0),
        ("abbc", 2, 4),
        # https://math.stackexchange.com/questions/73341/whats-the-general-expression-for-probability-of-a-failed-gift-exchange-draw
        ("aabbccddee", 13756, 440192),
    ],
)
def test_count_permutations_derangement(runner, sequence, expected, expected_if_same_distinct):
    result = runner.invoke(permutations, [sequence, "--constraints", "derangement"])
    assert result.output.rstrip() == str(expected)
    result = runner.invoke(
        permutations, [sequence, "--constraints", "derangement", "--same-distinct"]
    )
    assert result.output.rstrip() == str(expected_if_same_distinct)
