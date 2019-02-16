import pytest

from ccc.commands.count import multisets, draws


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
