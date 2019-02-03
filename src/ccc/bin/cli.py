import click

from ccc.commands.count import count
from ccc.commands.probability import probability


@click.group()
def ccc():
    """
    ccc

    Command-line Combinatorial Calculator to
    Count Constrained Collections.

    """
    pass


ccc.add_command(count)
ccc.add_command(probability)
