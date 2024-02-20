import logging
import sys

import pytest

from tg_bot.src.main import configure_logging


@pytest.mark.asyncio
async def test_configure_logging():
    configure_logging()

    fmt = '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s'
    logger = logging.getLogger()

    assert logger.level == logging.DEBUG
    assert logger.handlers[0].formatter._fmt == fmt
    assert logger.handlers[0].stream == sys.stdout
