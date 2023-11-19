import logging

from src.cli import cli

logging.basicConfig(
    level=logging.INFO,
    encoding="UTF-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

cli()
