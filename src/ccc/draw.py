from typing import AbstractSet, Dict, List, Optional, Tuple

from sympy import Poly, Rational, prod, binomial, factorial
from sympy.abc import x

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

        if self.replace:

            polys = []
            total = self.total_items_in_collection()

            for item, degrees in self._degrees.items():

                p = degrees_to_polynomial_with_fractional_coeff(
                    degrees, self._collection[item], total
                )
                polys.append(p)

            return prod(polys).coeff_monomial(x ** self._max_degree) * factorial(self._max_degree)

        return self.count() / binomial(self.total_items_in_collection(), self._max_degree)


def degrees_to_polynomial_with_binomial_coeff(degrees: AbstractSet[int], n: int) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient binomial(n, d):

        {0, 2, 5} -> bin(n, 5)*x**5 + bin(n, 2)*x**2 + 1

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = binomial(n, degree)

    return Poly.from_dict(degree_coeff_dict, x)


def degrees_to_polynomial(degrees: AbstractSet[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms having coefficient 1 (and all other terms zero), e.g.:

        {0, 2, 5} -> x**5 + x**2 + 1

    """
    degrees_dict = dict.fromkeys(degrees, 1)
    return Poly.from_dict(degrees_dict, x)


def degrees_to_polynomial_with_fractional_coeff(
    degrees: AbstractSet[int], n: int, total: int
) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having a rational coefficient (d / n)**n:

        {5} -> (n / total)**5 * x**5 / 5!

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = Rational(n, total) ** degree / factorial(degree)

    return Poly.from_dict(degree_coeff_dict, x)
