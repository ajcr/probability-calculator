from typing import Collection, Dict, List, Optional, Set, Tuple

from sympy import Poly, Rational, prod, binomial, factorial
from sympy.abc import x

from ccc.errors import ConstraintNotImplementedError


class MultisetCounter:
    """
    Count multisets of a given size that meet constraints.

    This count is computed by constructing polynomials with coefficients
    of particular terms equal to 1, and then multiplying these
    polynomials together and identifying the coefficient of the
    term with the specified degree.

    """

    def __init__(
        self,
        size: int,
        constraints: Optional[List[Tuple]] = None,
        collection: Optional[Dict[str, int]] = None,
    ) -> None:

        if constraints is None and collection is None:
            raise ValueError("Must specify 'constraints' or 'collection' or both")

        self._collection = collection
        self._max_degree = size

        self._degrees: Dict[str, Collection[int]] = {}

        # do not allow constraints on items that are not in the collection

        if collection is not None and constraints is not None:
            missing = _constraint_items_missing_from_collection(constraints, collection)
            if missing:
                raise ValueError(
                    f"The following items are not in the collection: {', '.join(missing)}"
                )

        # impose any contraints on the items in the possible multisets

        if constraints is not None:
            for op, *args in constraints:
                try:
                    getattr(self, "impose_constraint_" + op)(*args)
                except AttributeError:
                    raise ConstraintNotImplementedError(
                        f"Constraint '{op}' is not implemented"
                    ) from None

        # add items from the collection that were not constrained

        if collection is not None:
            for item, count in collection.items():
                if item not in self._degrees:
                    self.impose_constraint_le(item, count)

    def impose_constraint_eq(self, item: str, number: int) -> None:
        self.impose_constraint_in(item, [number])

    def impose_constraint_ne(self, item: str, number: int) -> None:
        self.impose_constraint_not_in(item, [number])

    def impose_constraint_lt(self, item: str, number: int) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(range(number))
        else:
            self._degrees[item] = set(range(number))

    def impose_constraint_le(self, item: str, number: int) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(range(number + 1))
        else:
            self._degrees[item] = set(range(number + 1))

    def impose_constraint_gt(self, item: str, number: int) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(range(number + 1, self._max_degree + 1))
        else:
            self._degrees[item] = set(range(number + 1, self._max_degree + 1))

    def impose_constraint_ge(self, item: str, number: int) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(range(number, self._max_degree + 1))
        else:
            self._degrees[item] = set(range(number, self._max_degree + 1))

    def impose_constraint_in(self, item: str, numbers: Collection[int]) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(numbers)
        else:
            self._degrees[item] = set(numbers)

    def impose_constraint_not_in(self, item: str, numbers: Collection[int]) -> None:
        if item in self._degrees:
            self._degrees[item] -= set(numbers)
        else:
            self._degrees[item] = set(range(self._max_degree + 1)) - set(numbers)

    def impose_constraint_mod(self, item: str, mod: int, rem: int) -> None:
        if item in self._degrees:
            self._degrees[item] &= set(range(rem, self._max_degree + 1, mod))
        else:
            self._degrees[item] = set(range(rem, self._max_degree + 1, mod))

    def total_items_in_collection(self) -> Optional[int]:
        """
        The total number of items in the collection, if given.
        """
        if self._collection is not None:
            return sum(self._collection.values())

    def count(self) -> int:
        """
        Number of possible multisets.
        """
        # multiply polynomials with fewer terms first
        degree_sets = sorted(self._degrees.values(), key=len)
        poly = prod(degrees_to_polynomial(degrees) for degrees in degree_sets)
        return poly.coeff_monomial(x ** self._max_degree)

    def draws(self) -> int:
        """
        Number of ways of drawing the multiset from the collection
        (without replacement).

        """
        if self._collection is not None:

            polys = []

            for item, degrees in self._degrees.items():

                p = degrees_to_polynomial_with_binomial_coeff(
                    degrees, self._collection[item]
                )
                polys.append(p)

            poly = prod(polys)
            return poly.coeff_monomial(x ** self._max_degree)

        else:
            raise ValueError("Cannot use 'draw' when collection is None")

    def draw_probability(self) -> Rational:
        """
        Probability of drawing the multiset from the collection
        (without replacement).

        """
        return self.draws() / binomial(
            self.total_items_in_collection(), self._max_degree
        )

    def sequence_count(self) -> int:
        """
        Number of possible distinct sequences
        """
        # multiply polynomials with fewer terms first
        degree_sets = sorted(self._degrees.values(), key=len)
        poly = prod(
            degrees_to_polynomial_with_factorial_coeff(degrees)
            for degrees in degree_sets
        )
        return poly.coeff_monomial(x ** self._max_degree) * factorial(self._max_degree)


def _constraint_items_missing_from_collection(
    constraints: List[Tuple], collection: Dict[str, int]
) -> Set[str]:
    """
    Determine the constrained items that are not specified
    in the collection.

    """
    constrained_items = set()

    for constraint in constraints:
        if len(constraint) > 1:
            constrained_items.add(constraint[1])

    return sorted(constrained_items - collection.keys())


def degrees_to_polynomial(degrees: Set[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms having coefficient 1 (and all other terms zero), e.g.:

        {0, 2, 5} -> x**5 + x**2 + 1

    """
    degrees_dict = dict.fromkeys(degrees, 1)
    return Poly.from_dict(degrees_dict, x)


def degrees_to_polynomial_with_binomial_coeff(degrees: Set[int], n: int) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient binomial(n, d):

        {0, 2, 5} -> bin(n, 5)*x**5 + bin(n, 2)*x**2 + 1

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = binomial(n, degree)

    return Poly.from_dict(degree_coeff_dict, x)


def degrees_to_polynomial_with_factorial_coeff(degrees: Set[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient 1/n!:

        {0, 2, 5} -> x**5 / 5! + x**2 / 2!  + 1 / 1!

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = 1 / factorial(degree)

    return Poly.from_dict(degree_coeff_dict, x)
