import ast
from typing import List, Tuple, Union

from ccc.errors import ConstraintError

# Mappings for ast node classes to strings

CONTAINS_OPS = {ast.In: "in", ast.NotIn: "not_in"}
EQUALITIES = {ast.Eq: "eq", ast.NotEq: "ne"}
ORDER_OPS = {ast.Lt: "lt", ast.LtE: "le", ast.Gt: "gt", ast.GtE: "ge", **EQUALITIES}
REFLECT_ORDER_OPS = {ast.Lt: "gt", ast.LtE: "ge", ast.Gt: "lt", ast.GtE: "le", **EQUALITIES}

# Constraint Type Annotations

CompareConstraint = Tuple[str, str, int]
ContainsConstraint = Tuple[str, str, List[int]]
ModConstraint = Tuple[str, str, int, int]
NameConstraint = Tuple[str]

OrderOpConstraintConjunctionList = List[Union[CompareConstraint, ContainsConstraint, ModConstraint]]


def process_single_compare_node(
    compare_node: ast.Compare
) -> Union[CompareConstraint, ContainsConstraint, ModConstraint]:
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
    op = compare_node.ops[0]

    if type(op) in ORDER_OPS:

        # see if compare is of form 'item __op__ num'

        try:
            return (
                ORDER_OPS[type(op)],
                compare_node.left.id,  # type: ignore
                compare_node.comparators[0].n,  # type: ignore
            )

        except (AttributeError, TypeError):
            pass

        # see if compare is of form 'num __op__ item' (inequalities must be swapped)

        try:
            return (
                REFLECT_ORDER_OPS[type(op)],
                compare_node.comparators[0].id,  # type: ignore
                compare_node.left.n,  # type: ignore
            )

        except (AttributeError, TypeError):
            pass

        # see if compare is of form 'item % mod == rem'

        try:
            if isinstance(compare_node.left.op, ast.Mod) and isinstance(  # type: ignore
                compare_node.ops[0], ast.Eq
            ):
                item = compare_node.left.left.id  # type: ignore
                mod = compare_node.left.right.n  # type: ignore
                rem = compare_node.comparators[0].n  # type: ignore
                return "mod", item, mod, rem

        except (AttributeError, TypeError):
            # fall through to error
            pass

    elif type(op) in CONTAINS_OPS:

        # see if compare is of form 'item in (3, 5, 7)' or 'item not in (3, 5, 7)'

        try:
            item = compare_node.left.id  # type: ignore
            nums = [num.n for num in compare_node.comparators[0].elts]  # type: ignore
            return CONTAINS_OPS[type(op)], item, nums

        except (AttributeError, TypeError):
            # fall through to error
            pass

    raise ConstraintError(f"Constraint starting at offset {compare_node.col_offset} not understood")


def process_chained_compare_node(compare_node: ast.Compare) -> OrderOpConstraintConjunctionList:
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
    op1, op2 = compare_node.ops

    try:
        if {type(op1), type(op2)} < ORDER_OPS.keys() - EQUALITIES.keys():
            return [
                (
                    REFLECT_ORDER_OPS[type(op1)],
                    compare_node.comparators[0].id,  # type: ignore
                    compare_node.left.n,  # type:ignore
                ),
                (
                    ORDER_OPS[type(op2)],
                    compare_node.comparators[0].id,  # type: ignore
                    compare_node.comparators[1].n,  # type: ignore
                ),
            ]

    except (AttributeError, TypeError):
        pass

    raise ConstraintError(f"Constraint starting at offset {compare_node.col_offset} not understood")


def process_compare_node(compare_node: ast.Compare) -> OrderOpConstraintConjunctionList:
    """
    Unpack a compare node into constraints.

    """
    n: int = len(compare_node.comparators)

    if n == 1:
        return [process_single_compare_node(compare_node)]

    if n == 2:
        return process_chained_compare_node(compare_node)

    raise ConstraintError(
        f"Constraint at offset {compare_node.col_offset} contains"
        " chained comparison longer than two"
    )


def process_tuple_node(tuple_node: ast.Tuple) -> List:
    """
    Visit and process each constraint in the tuple.

    Each constraint can be either a compare operateration or a name.
    """
    constraints: List = []

    for node in tuple_node.elts:

        if isinstance(node, ast.Compare):
            constraints += process_compare_node(node)

        elif isinstance(node, ast.Name):
            constraints += [(node.id,)]

        else:
            raise ConstraintError(f"Unknown constraint in tuple at offset {node.col_offset}")

    return constraints


def process_boolop_node(boolop_node: ast.BoolOp) -> List:
    """
    Disjunctions ('or') of tuples, comparisions or names are supported.

    Boolean operations are not permitted within disjuncts.
    """
    disjunctions: List = []

    for node in boolop_node.values:

        if isinstance(node, ast.Tuple):
            disjunctions += [process_tuple_node(node)]

        elif isinstance(node, ast.Compare):
            disjunctions += [process_compare_node(node)]

        elif isinstance(node, ast.Name):
            disjunctions += [[(node.id,)]]

        else:
            raise ConstraintError(f"Invalid constraint in disjunction at offset {node.col_offset}")

    return disjunctions


def process_constraint_string(constraint_string: str) -> List:
    """
    Parse and process a string representing the collection constraints.

    Conjuncts must be expressed as a tuple and can be comparison
    operations or names.

    Single comparision operations and names are also permitted.

    Disjunctions ('or') of tuples, comparisions or names are supported.
    """
    try:
        body = ast.parse(constraint_string).body

    except SyntaxError:
        raise ConstraintError("Invalid syntax in constraint string") from None

    if body:
        node = body[0].value  # type: ignore

    else:
        raise ConstraintError("Empty constraint string")

    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        return process_boolop_node(node)

    if isinstance(node, ast.Tuple):
        return [process_tuple_node(node)]

    if isinstance(node, ast.Compare):
        return [process_compare_node(node)]

    if isinstance(node, ast.Name):
        return [[(node.id,)]]

    raise ConstraintError(f"Invalid constraint: {constraint_string}")
