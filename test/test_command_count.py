import pytest

from ccc.commands.count import multisets, sequences, permutations


@pytest.mark.parametrize("size,constraints,expected", [
    # https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/
    # 6-042j-mathematics-for-computer-science-fall-2005/readings/ln11.pdf
    (6, "apple % 2 == 0, orange <= 4, pear in (0, 1), banana % 5 == 0", 7),
    (100, "apple % 2 == 0, orange <= 4, pear in (0, 1), banana % 5 == 0", 101),
    # https://projecteuler.net/problem=31
    (200, "a%1==0, b%2==0, c%5==0, d%10==0, e%20==0, f%50==0, g%100==0, h%200==0", 73682),
])
def test_count_multisets(runner, size, constraints, expected):
    result = runner.invoke(multisets, ["--size", size, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize("size,constraints,expected", [
    (4, "f == 1, o == 2, d == 1", 12),
    # https://math.stackexchange.com/questions/960046
    (3, "a <= 2, b <= 3", 7),
    (3, "m <= 1, p <= 2, i <= 4, s <= 4", 53),
])
def test_count_sequences(runner, size, constraints, expected):
    result = runner.invoke(sequences, ["--size", size, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)


@pytest.mark.parametrize("sequence,constraints,expected", [
    ("food", None, 12),
    ("food", "no_adjacent", 6),
    ("food", "derangement", 2),
    ("mississippi", "no_adjacent", 2016),
])
def test_count_permutations(runner, sequence, constraints, expected):
    if constraints is None:
        result = runner.invoke(permutations, [sequence])
    else:
        result = runner.invoke(permutations, [sequence, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)
