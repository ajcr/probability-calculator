import ast
from typing import Dict, Tuple


def unpack_assign(assign: ast.Assign) -> Tuple[str, int]:
    """
    Unpack an assignment into a (target, value) tuple.

    """
    try:
        targets = assign.targets
        value = assign.value.n

    except (AttributeError, TypeError):
        raise ValueError(f"Item count at {assign.col_offset} not understood") from None

    if len(targets) > 1:
        raise ValueError(f"Can only assign count to single item, not {','.join(targets)}")

    if not isinstance(value, int) or value < 1:
        raise ValueError(f"Item counts must be positive integers, got {value}")

    return targets[0].id, value


def process_collection_string(collection_string: str) -> Dict[str, int]:
    """
    Parse and process a string with counts of items in the collection.

        red = 3; blue = 7; yellow = 5

    """
    item_counts: Dict[str, int] = {}

    nodes = ast.parse(collection_string).body

    for node in nodes:

        if isinstance(node, ast.Assign):
            item, count = unpack_assign(node)

        else:
            raise ValueError(f"Invalid item assignment in string")

        if item in item_counts:
            raise ValueError(f"Item '{item}' has multiple counts assigned")

        else:
            item_counts[item] = count

    return item_counts
