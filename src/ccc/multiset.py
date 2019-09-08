from typing import AbstractSet, Dict, List, Optional, Tuple

from sympy import Poly, prod
from sympy.abc import x

from ccc.polynomialtracker import PolynomialTracker


class Multiset(PolynomialTracker):
    """
    Track multisets that meet zero or more constraints.

    """

    def __init__(
        self,
        size: int,
        collection: Optional[Dict[str, int]] = None,
        constraints: Optional[List[Tuple]] = None,
    ) -> None:

        if constraints is None and collection is None:
            raise ValueError("Must specify either 'constraints', 'collection', or both")

        super().__init__(size, collection, constraints)

    def count(self) -> int:
        """
        Count number of possible multisets that meet constraints.
        """
        poly = prod(degrees_to_polynomial(degrees) for degrees in self._degrees.values())
        return poly.coeff_monomial(x ** self._max_degree)


def degrees_to_polynomial(degrees: AbstractSet[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms having coefficient 1 (and all other terms zero), e.g.:

        {0, 2, 5} -> x**5 + x**2 + 1

    """
    degrees_dict = dict.fromkeys(degrees, 1)
    return Poly.from_dict(degrees_dict, x)
