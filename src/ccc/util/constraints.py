import ast
from typing import List, Tuple

# Mappings for ast node classes to strings

CONTAINS_OPS = {
    ast.In: "in",
    ast.NotIn: "not_in",
}

EQUALITIES = {
    ast.Eq: "eq",
    ast.NotEq: "ne",
}

ORDER_OPS = {
    ast.Lt: 'lt',
    ast.LtE: 'le',
    ast.Gt: 'gt',
    ast.GtE: 'ge',
    **EQUALITIES,
}

REFLECT_ORDER_OPS = {
    ast.Lt: 'gt',
    ast.LtE: 'ge',
    ast.Gt: 'lt',
    ast.GtE: 'le',
    **EQUALITIES,
}


def unpack_single_compare_operation(compare: ast.Compare) -> Tuple:
    """
    Unpack a compare operation into its constituent parts.

    Currently supports comparisons using the operators
    ==, !=, <, <=, >, >= that take either of the forms:

        item __op__ num
        num __op__ item

    or comparisons using __contains__ (in):

        item in (3, 5, 7)
        item not in [1, 2, 4, 8]

    or comparisons where the left-hand side is a binary
    modulo operation, such as:

        item % mod == rem

    """
    op = compare.ops[0]

    if type(op) in ORDER_OPS:

        # see if compare is of form 'item __op__ num'

        try:
            return ORDER_OPS[type(op)], compare.left.id, compare.comparators[0].n

        except (AttributeError, TypeError):
            pass

        # see if compare is of form 'num __op__ item' (inequalities must be swapped)

        try:
            return REFLECT_ORDER_OPS[type(op)], compare.comparators[0].id, compare.left.n

        except (AttributeError, TypeError):
            pass

        # see if compare is of form 'item % mod == rem'

        try:
            if isinstance(compare.left.op, ast.Mod) and isinstance(compare.ops[0], ast.Eq):
                item = compare.left.left.id
                mod = compare.left.right.n
                rem = compare.comparators[0].n
                return "mod", item, mod, rem

        except (AttributeError, TypeError):
            # fall through to error
            pass

    elif type(op) in CONTAINS_OPS:

        # see if compare is of form 'item in (3, 5, 7)' or 'item not in (3, 5, 7)'

        try:
            item = compare.left.id
            nums = [num.n for num in compare.comparators[0].elts]
            return CONTAINS_OPS[type(op)], item, nums

        except (AttributeError, TypeError):
            # fall through to error
            pass

    raise ValueError(f"Constraint starting at offset {compare.col_offset} not understood")


def unpack_chained_compare_operation(compare: ast.Compare) -> Tuple:
    """
    Unpack a chained compare operation into its two
    constituent parts.

    Currently supports comparisons using the operators
    <, <=, >, >= that take the form:

        num1 __op1__ item __op2__ num2

    This expression is treated as

        num1 __op1__ item
        item __op2__ num2

    N.B. the == and != operators are not permitted.
    """
    op1, op2 = compare.ops

    try:
        if {type(op1), type(op2)} < ORDER_OPS.keys() - EQUALITIES.keys():
            return [
                (REFLECT_ORDER_OPS[type(op1)], compare.comparators[0].id, compare.left.n),
                (ORDER_OPS[type(op2)], compare.comparators[0].id, compare.comparators[1].n),
            ]

    except (AttributeError, TypeError):
        pass

    raise ValueError(f"Constraint starting at offset {compare.col_offset} not understood")


def unpack_compare(compare: ast.Compare) -> List[Tuple]:
    """
    Unpack a compare node into constraints.

    """
    n: int = len(compare.comparators)

    if n == 1:
        return [unpack_single_compare_operation(compare)]

    elif n == 2:
        return unpack_chained_compare_operation(compare)

    else:
        raise ValueError(
            f"Constraint at offset {compare.col_offset} contains"
            " chained comparison longer than two"
        )


def process_constraints_in_tuple(constraint_tuple: ast.Tuple) -> List[Tuple]:
    """
    Visit and process each constraint in the tuple.

    """
    constraints: List = []

    for node in constraint_tuple.elts:

        if isinstance(node, ast.Compare):
            constraints += unpack_compare(node)

        elif isinstance(node, ast.Name):
            constraints += [(node.id,)]

        else:
            raise ValueError("Unknown constraint in tuple")

    return constraints


def process_constraint_string(constraint_string: str) -> List[Tuple]:
    """
    Parse and process a string representing the collection constraints.

    Currently, only conjunction of constraints is supported.
    Conjuncts must be expressed as a tuple and can be comparison
    operations or names.

    Single comparision operations and names are also permitted.
    """
    node = ast.parse(constraint_string).body[0].value

    if isinstance(node, ast.Tuple):
        return process_constraints_in_tuple(node)

    elif isinstance(node, ast.Compare):
        return unpack_compare(node)

    elif isinstance(node, ast.Name):
        return [(node.id,)]

    else:
        raise ValueError(f"Invalid constraint(s): {constraint_string}")
