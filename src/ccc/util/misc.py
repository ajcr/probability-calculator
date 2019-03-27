from itertools import chain, combinations
from typing import List, Sequence, Generator, TypeVar, Tuple

T = TypeVar("T")


def subsets(seq: Sequence[Sequence[T]]) -> Generator[Tuple[int, List[T]], None, None]:
    """
    Generate all non-empty subsets of a sequence of sequences,
    merged into a single sequence.

    Each merged sequence is returned, along with the number of
    subsets that were merged.

    """
    for n in range(1, len(seq) + 1):
        combs = combinations(seq, n)
        for cmb in combs:
            yield n, list(chain.from_iterable(cmb))
