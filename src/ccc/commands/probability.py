from fractions import Fraction
from typing import List, Dict, Tuple

import click

from ccc.multiset import MultisetCounter
from ccc.permutation import PermutationCounter
from ccc.util.constraints import process_constraint_string
from ccc.util.collection import process_collection_string
from ccc.util.misc import subsets


@click.group()
def probability() -> None:
    """
    Compute the probability that a specified collection is seen.

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
        answer = 0

        for n, subset in subsets(constraints):
            ms = MultisetCounter(size, subset, collection)
            answer += (-1) ** (n + 1) * ms.draw_probability()

    if rational:
        click.echo(answer)
    else:
        click.echo(float(answer))


@probability.command()
@click.argument("sequence")
@click.option("--constraints", "-c", type=str, required=True)
@click.option("--same-distinct/--no-same-distinct", default=False)
@click.option("--rational/--float", default=True)
def permutation(sequence, constraints, same_distinct, rational):
    """
    Probability that a random permutation of the sequence
    meets a specified contraint.
    """
    constraints = process_constraint_string(constraints)

    if len(constraints) > 1:
        sys.exit("Using 'or' is not supported for permutations")

    constraints = constraints[0]

    permutation = PermutationCounter(sequence, constraints, same_distinct)
    answer = permutation.probability()

    if rational:
        click.echo(answer)
    else:
        click.echo(float(answer))
