from typing import Optional, Collection, Dict, List, Tuple, MutableSet

from ccc.errors import ConstraintNotImplementedError


class PolynomialTracker:
    """
    Base class implementing methods for creating and modifying
    polynomials based on constraints.

    """

    def __init__(
        self,
        size: int,
        collection: Optional[Dict[str, int]] = None,
        constraints: Optional[List[Tuple]] = None,
    ) -> None:
        self.size = size
        self._max_degree = size
        self._collection = collection
        self._constraints = constraints
        self._degrees: Dict[str, MutableSet[int]] = {}

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
        self._add_unconstrained_items()

    def _add_unconstrained_items(self) -> None:
        if self._collection is not None:
            for item, count in self._collection.items():
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

        return None


def _constraint_items_missing_from_collection(
    constraints: List[Tuple], collection: Dict[str, int]
) -> List[str]:
    """
    Determine the constrained items that are not specified
    in the collection.

    """
    constrained_items = set()

    for constraint in constraints:
        if len(constraint) > 1:
            constrained_items.add(constraint[1])

    return sorted(constrained_items - collection.keys())
