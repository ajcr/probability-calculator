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
@click.option("--constraints", "-c", type=str)
@click.option("--collection", "-k", type=str, required=True)
@click.option("--rational/--float", default=True)
def draw(size, constraints, collection, rational) -> None:
    """
    Probability of drawing (without replacement) a collection
    of the specified size from the specified collection that
    optionally meets one or more contraints.
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    collection = process_collection_string(collection)

    if len(constraints) == 1:
        ms = MultisetCounter(size, constraints[0], collection)
        answer = ms.draw_probability()

    else:
        click.echo("Not Implemented")

    if rational:
        click.echo(answer)
    else:
        click.echo(float(answer))
