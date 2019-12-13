import sys

import click

from ccc.draw import Draw
from ccc.permutation import PermutationCounter
from ccc.util.constraints import process_constraint_string
from ccc.util.collection import process_collection_string
from ccc.util.misc import subsets


@click.group()
def probability() -> None:
    "Probability that a collection of items is drawn"


@probability.command("draw")
@click.option("--number", "-n", type=int, required=True, help="Number of items to draw")
@click.option(
    "--from", "-f", "from_", type=str, required=True, help="Collection of items to draw from"
)
@click.option("--constraints", "-c", type=str, required=True, help="Constraints the draw must meet")
@click.option(
    "--replace/--no-replace",
    default=False,
    help="Toggle whether each item is replaced after being drawn",
)
@click.option("--rational/--float", default=True, help="Toggle representation of probability")
def draw_command(number, constraints, from_, rational, replace) -> None:
    """
    Probability of drawing a collection a given size such that
    any constraints imposed on the items are met
    """
    if constraints is not None:
        constraints = process_constraint_string(constraints)

    collection = process_collection_string(from_)

    if len(constraints) == 1:
        draw = Draw(number, collection, constraints[0], replace=replace)
        answer = draw.probability()

    else:
        answer = 0

        # Inclusion/Exclusion
        for n, subset in subsets(constraints):
            draw = Draw(number, collection, subset, replace=replace)
            answer += (-1) ** (n + 1) * draw.probability()

    if rational:
        click.echo(answer)
    else:
        click.echo(float(answer))


@probability.command("permutation")
@click.argument("sequence")
@click.option(
    "--constraints", "-c", type=str, required=True, help="Constraints the permuation must meet"
)
@click.option(
    "--same-distinct/--no-same-distinct", default=False, help="Toggle whether each item is unique"
)
@click.option("--rational/--float", default=True, help="Toggle representation of probability")
def permutation_command(sequence, constraints, same_distinct, rational):
    """
    Probability that a random permutation of the given sequence
    meets the specified contraints.
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
