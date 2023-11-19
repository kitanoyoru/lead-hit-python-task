import click

from .commands.reset_db_command import reset_db


@click.group()
def cli():
    pass


cli.add_command(reset_db)
