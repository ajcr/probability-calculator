from typing import Optional, Dict, List, Tuple, AbstractSet

from sympy import Poly, prod, factorial
from sympy.abc import x

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


def degrees_to_polynomial_with_factorial_coeff(degrees: AbstractSet[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient 1/n!:

        {0, 2, 5} -> x**5 / 5! + x**2 / 2!  + 1 / 1!

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = 1 / factorial(degree)

    return Poly.from_dict(degree_coeff_dict, x)
