import ast
from typing import Dict, Tuple

from ccc.errors import CollectionError


def unpack_assign(assign: ast.Assign) -> Tuple[str, int]:
    """
    Unpack an assignment into a (target, value) tuple.

    """
    try:
        targets = assign.targets
        value = assign.value.n  # type: ignore

    except (AttributeError, TypeError):
        raise CollectionError(f"Item count at {assign.col_offset} not understood") from None

    if len(targets) > 1:
        raise CollectionError(
            f"Can only assign count to single item, not {','.join(targets)}"  # type: ignore
        )

    if not isinstance(value, int) or value < 1:
        raise CollectionError(f"Item counts must be positive integers, got {value}")

    return targets[0].id, value  # type: ignore


def process_collection_string(collection_string: str) -> Dict[str, int]:
    """
    Parse and process a string with counts of items in the collection.

        "red = 3; blue = 7; yellow = 5"

    becomes:

        {"red": 3, "blue": 7, "yellow": 5}

    """
    item_counts: Dict[str, int] = {}

    nodes = ast.parse(collection_string).body

    for node in nodes:

        if isinstance(node, ast.Assign):
            item, count = unpack_assign(node)

        else:
            raise CollectionError(f"Invalid item assignment in string at offset {node.col_offset}")

        if item not in item_counts:
            item_counts[item] = count

        else:
            raise CollectionError(f"Item '{item}' has multiple counts assigned")

    return item_counts
