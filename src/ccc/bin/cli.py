import click

from ccc.commands.count import count
from ccc.commands.probability import probability


ALIASES = {"prob": probability}


# pylint: disable=too-few-public-methods
class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup)
def ccc():
    """
    ccc

    Command-line Combinatorial Calculator to
    Count Constrained Collections.

    """


ccc.add_command(count)
ccc.add_command(probability)
