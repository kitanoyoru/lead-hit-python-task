import click

from .commands.start_server_command import start_server


@click.group()
def cli():
    pass


cli.add_command(start_server)
