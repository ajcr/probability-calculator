from fractions import Fraction
from typing import List, Dict, Tuple

import click

from ccc.multiset import MultisetCounter
from ccc.util.constraints import process_constraint_string
from ccc.util.collection import process_collection_string


@click.group()
def probability() -> None:
    """
    Count the number of object that match the given constraints.

    """
    pass


@probability.command()
@click.option("--size", "-s", type=int, required=True)
@click.option("--constraints", "-c", type=str, required=True)
@click.option("--collection", "-k", type=str, required=True)
def draw(size, constraints, collection) -> None:
    """
    Compute the probability of choosing, from a given collection,
    size-many items that meet the constraint criteria.
    """
    #processed_constraints: List[Tuple] = process_constraint_string(constraints)
    #collection_items: Dict[str, int] = process_collection_string(collection)

    click.echo("not yet implemented")
