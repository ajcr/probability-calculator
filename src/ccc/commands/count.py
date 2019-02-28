import sys

import click

from ccc.multiset import MultisetCounter
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
        ms = MultisetCounter(size, constraints[0], collection)
        answer = ms.count()

    else:
        if collection is None:
            sys.exit("Must specify a collection if using 'or' in constraints")

        answer = 0

        for n, subset in subsets(constraints):
            ms = MultisetCounter(size, subset, collection)
            answer += (-1)**(n+1) * ms.count()

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
        ms = MultisetCounter(size, constraints[0], collection)
        answer = ms.draws()

    else:
        answer = 0

        for n, subset in subsets(constraints):
            ms = MultisetCounter(size, subset, collection)
            answer += (-1)**(n+1) * ms.draws()

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
        ms = MultisetCounter(size, constraints[0], collection)
        answer = ms.sequence_count()

    else:
        if collection is None:
            sys.exit("Must specify a collection if using 'or' in constraints")

        answer = 0

        for n, subset in subsets(constraints):
            ms = MultisetCounter(size, subset, collection)
            answer += (-1)**(n+1) * ms.sequence_count()

    click.echo(answer)
