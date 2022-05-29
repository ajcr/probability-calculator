from typing import Dict, List, Optional, Tuple

from sympy import prod
from sympy.abc import x

from ccc.polynomial import degrees_to_polynomial
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
