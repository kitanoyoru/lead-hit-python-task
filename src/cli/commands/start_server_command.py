import logging

import click
import uvicorn

logger = logging.getLogger(__name__)


@click.command()
def start_server():
    uvicorn.run(
        "src.main:create_app",
        host="0.0.0.0",
        port=8000,
        factory=True,
        reload=True,
        log_config="./config/log_conf.yaml",
    )
