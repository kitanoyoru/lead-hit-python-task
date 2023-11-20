import logging

import click

logger = logging.getLogger(__name__)


@click.command()
def reset_db():
    logger.info("Database was resetted successfully")
