import pytest

from ccc.commands.probability import draw, permutation


@pytest.mark.parametrize("size,constraints,collection,expected", [
    # https://math.stackexchange.com/questions/898683
    (8, "r>=1,b>=1,g>=1,w>=1,bl>=1,gr>=1", "r=5;b=5;g=5;w=5;bl=5;gr=5", "5000/26013"),
    # https://math.stackexchange.com/questions/897730
    (6, "r >= 1, g >= 1", "r=10; g=10", "639/646"),
    # https://math.stackexchange.com/questions/2979053
    (4, "(r==2, w==2) or (r==2, b==2) or (b==2, w==2)", "w=25;r=2;b=3", "401/9135"),
    # https://math.stackexchange.com/questions/334516
    (3, "r==3 or g==3 or b==3", "r=3; g=4; b=5", "3/44"),
    
])
def test_count_multisets(runner, size, constraints, collection, expected):
    result = runner.invoke(draw, ["--size", size, "--constraints", constraints, "--collection", collection])
    assert result.output.rstrip() == expected


@pytest.mark.parametrize("sequence,constraints,expected", [
    ("food", "no_adjacent", "1/2"),
    ("food", "derangement", "1/6"),
])
def test_count_permutations(runner, sequence, constraints, expected):
    result = runner.invoke(permutation, [sequence, "--constraints", constraints])
    assert result.output.rstrip() == str(expected)
