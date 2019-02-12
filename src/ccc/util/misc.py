from itertools import chain, combinations
from typing import List, Sequence, Generator, TypeVar

T = TypeVar('T')

def subsets(x: Sequence[List[T]]) -> Generator[List[T], None, None]:
    """

    """
    for n in range(1, len(x) + 1):
        combs = combinations(x, n)
        for cmb in combs:
            yield n, list(chain.from_iterable(cmb))
