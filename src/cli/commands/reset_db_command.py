import logging

import click

from src.config import get_database_url
from src.database import reset_database

logger = logging.getLogger(__name__)


@click.command()
def reset_db():
    database_url = get_database_url()
    reset_database(database_url)
    logger.info("Database was resetted successfully")
