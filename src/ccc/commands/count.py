import sys

import click

from ccc.draw import Draw
from ccc.multiset import Multiset
from ccc.sequence import Sequence
from ccc.permutation import PermutationCounter
from ccc.util.constraints import process_constraint_string
from ccc.util.collection import process_collection_string
from ccc.util.misc import subsets


@click.group()
def count():
    "Count how many objects of the given type meet the constraints"


@count.command()
@click.option("--size", "-s", type=int, required=True, help="Number of items in multiset")
@click.option("--collection", "-k", type=str, help="Collection to produce multisets from")
@click.option("--constraints", "-c", type=str, help="Constraints on items in multiset")
def multisets(size, constraints, collection):
    """
    Count multisets of the given size that meet zero or more constraints
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    if collection is not None:
        collection = process_collection_string(collection)

    if len(constraints) == 1:
        ms = Multiset(size, collection, constraints[0])
        answer = ms.count()

    else:
        if collection is None:
            sys.exit("Must specify a collection if using 'or' in constraints")

        answer = 0

        # Inclusion/Exclusion
        for n, subset in subsets(constraints):
            ms = Multiset(size, collection, subset)
            answer += (-1) ** (n + 1) * ms.count()

    click.echo(answer)


@count.command()
@click.option("--size", "-s", type=int, required=True, help="Number of items to draw")
@click.option("--collection", "-k", type=str, required=True, help="Collection to draw from")
@click.option("--constraints", "-c", type=str, help="Constraints on drawn items")
def draws(size, constraints, collection):
    """
    Count draws (without replacement) of the given size from a
    collection which meet zero or more constraints
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    collection = process_collection_string(collection)

    if len(constraints) == 1:
        draw = Draw(size, collection, constraints[0])
        answer = draw.count()

    else:
        answer = 0

        # Inclusion/Exclusion
        for n, subset in subsets(constraints):
            draw = Draw(size, collection, subset)
            answer += (-1) ** (n + 1) * draw.count()

    click.echo(answer)


@count.command()
@click.option("--size", "-s", type=int, required=True, help="Number of items in sequence")
@click.option("--constraints", "-c", type=str, required=True, help="Constraints on sequences")
@click.option("--collection", "-k", type=str, help="Collection to create sequences from")
def sequences(size, constraints, collection):
    """
    Count possible sequences of the given size that meet zero more constraints
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    if collection is not None:
        collection = process_collection_string(collection)

    if len(constraints) == 1:
        seq = Sequence(size, collection, constraints[0])
        answer = seq.count()

    else:
        if collection is None:
            sys.exit("Must specify a collection if using 'or' in constraints")

        answer = 0

        # Inclusion/Exclusion
        for n, subset in subsets(constraints):
            seq = Sequence(size, collection, subset)
            answer += (-1) ** (n + 1) * seq.count()

    click.echo(answer)


@count.command()
@click.argument("sequence")
@click.option("--constraints", "-c", type=str, help="Constraints on permutations")
@click.option(
    "--same-distinct/--no-same-distinct", default=False, help="Toggle whether each item is unique"
)
def permutations(sequence, constraints, same_distinct):
    """
    Count permutations of the given sequence that that meet a constraint
    """
    if constraints is not None:

        constraints = process_constraint_string(constraints)

        if len(constraints) > 1:
            sys.exit("Using 'or' is not supported for permutations")

        constraints = constraints[0]

    permutation = PermutationCounter(sequence, constraints, same_distinct)
    answer = permutation.count()

    click.echo(answer)
