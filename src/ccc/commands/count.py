import click

from ccc.multiset import MultisetCounter
from ccc.util.constraints import process_constraint_string
from ccc.util.collection import process_collection_string


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

    ms = MultisetCounter(size, constraints, collection)

    answer = ms.count()

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

    ms = MultisetCounter(size, constraints, collection)

    answer = ms.draws()

    click.echo(answer)


@count.command()
@click.option("--size", "-s", type=int, required=True)
@click.option("--constraints", "-c", type=str)
def permutations(size, constraints):
    """
    Count permutations
    """
    pass
