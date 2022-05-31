from typing import Dict, List, Optional, Tuple

from sympy import Rational, prod, binomial, factorial
from sympy.abc import x

from ccc.polynomial import (
    degrees_to_polynomial_with_binomial_coeff,
    degrees_to_polynomial_with_fractional_coeff,
)
from ccc.polynomialtracker import PolynomialTracker


class Draw(PolynomialTracker):
    """
    Track ways of drawing items from the collection
    such that any constraints are met.

    """

    def __init__(
        self,
        size: int,
        collection: Dict[str, int],
        constraints: Optional[List[Tuple]] = None,
        replace: bool = False,
    ) -> None:

        if not collection:
            raise ValueError("collection cannot be empty")

        self.replace = replace
        super().__init__(size, collection, constraints)

    def _add_unconstrained_items(self) -> None:
        """
        If drawing with replacement, unconstrained items are not limited
        to their frequency in the collection.
        """
        if self.replace:
            for item in self._collection:
                if item not in self._degrees:
                    self.impose_constraint_le(item, self._max_degree)

        else:
            super()._add_unconstrained_items()

    def count(self) -> int:
        """
        Count number of draws that meet constraints.
        """
        polys = []

        for item, degrees in self._degrees.items():

            p = degrees_to_polynomial_with_binomial_coeff(degrees, self._collection[item])
            polys.append(p)

        return prod(polys).coeff_monomial(x ** self._max_degree)

    def probability(self) -> Rational:
        """
        Probability of drawing from the collection such that the
        constraints are met.
        """

        if not self.replace:
            return self.count() / binomial(self.total_items_in_collection(), self._max_degree)

        polys = []
        total = self.total_items_in_collection()

        for item, degrees in self._degrees.items():

            p = degrees_to_polynomial_with_fractional_coeff(degrees, self._collection[item], total)
            polys.append(p)

        return prod(polys).coeff_monomial(x ** self._max_degree) * factorial(self._max_degree)
