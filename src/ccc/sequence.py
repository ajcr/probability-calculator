from typing import Optional, Dict, List, Tuple

from sympy import prod, factorial
from sympy.abc import x

from ccc.polynomial import degrees_to_polynomial_with_factorial_coeff
from ccc.polynomialtracker import PolynomialTracker


class Sequence(PolynomialTracker):
    """
    Track sequences that meet specific constraints.

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
        Count number of sequences that meet constraints.
        """
        poly = prod(
            degrees_to_polynomial_with_factorial_coeff(degrees)
            for degrees in self._degrees.values()
        )
        return poly.coeff_monomial(x ** self._max_degree) * factorial(self._max_degree)
