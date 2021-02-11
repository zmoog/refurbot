import logging

from typing import Any, Dict

from refurbot import config, bootstrap
from refurbot.domain import commands

app_logger = logging.getLogger()
app_logger.setLevel(config.LOG_LEVEL)

logger = logging.getLogger(__name__)

messagebus = bootstrap.for_lambda()



def run_scheduled(event: Dict, config: Any):
    logger.info(f"Hello, I'm scheduled and just received this event: {event}!")

    cmd = commands.SearchDeals(
        country='us',
        product='mac'
    )

    messagebus.handle(cmd, {})
