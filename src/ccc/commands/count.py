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
    """
    Count the number of object that match the given constraints

    """
    pass


@count.command()
@click.option("--size", "-s", type=int, required=True)
@click.option("--constraints", "-c", type=str)
@click.option("--collection", "-k", type=str)
def multisets(size, constraints, collection):
    """
    Count multisets of the specified size that optionally
    meet one or more contraints.
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

        for n, subset in subsets(constraints):
            ms = Multiset(size, collection, subset)
            answer += (-1) ** (n + 1) * ms.count()

    click.echo(answer)


@count.command()
@click.option("--size", "-s", type=int, required=True)
@click.option("--constraints", "-c", type=str)
@click.option("--collection", "-k", type=str, required=True)
def draws(size, constraints, collection):
    """
    Number of possible draws (without replacement) of the
    specified size from the specified collection that
    optionally meet one or more contraints.
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    collection = process_collection_string(collection)

    if len(constraints) == 1:
        draw = Draw(size, collection, constraints[0])
        answer = draw.count()

    else:
        answer = 0

        for n, subset in subsets(constraints):
            draw = Draw(size, collection, subset)
            answer += (-1) ** (n + 1) * draw.count()

    click.echo(answer)


@count.command()
@click.option("--size", "-s", type=int, required=True)
@click.option("--constraints", "-c", type=str)
@click.option("--collection", "-k", type=str)
def sequences(size, constraints, collection):
    """
    Number of possible sequences of the specified size
    that optionally meet one or more contraints.
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

        for n, subset in subsets(constraints):
            seq = Sequence(size, collection, subset)
            answer += (-1) ** (n + 1) * seq.count()

    click.echo(answer)


@count.command()
@click.argument("sequence")
@click.option("--constraints", "-c", type=str)
@click.option("--same-distinct/--no-same-distinct", default=False)
def permutations(sequence, constraints, same_distinct):
    """
    Number of possible permutations of the sequence that
    that optionally meet a specified contraint.
    """
    if constraints is not None:

        constraints = process_constraint_string(constraints)

        if len(constraints) > 1:
            sys.exit("Using 'or' is not supported for permutations")

        constraints = constraints[0]

    permutation = PermutationCounter(sequence, constraints, same_distinct)
    answer = permutation.count()

    click.echo(answer)
