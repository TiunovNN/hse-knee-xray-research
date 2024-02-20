import os

import pytest

from tg_bot.src.main import Config


@pytest.mark.asyncio
async def test_config():
    with pytest.raises(ValueError, match='Please, set BOT_TOKEN'):
        Config.from_env()

    os.environ['BOT_TOKEN'] = 'bot_token'

    with pytest.raises(ValueError, match='Please, set BOT_API_URL'):
        Config.from_env()

    os.environ['BOT_API_URL'] = 'bot_api_url'
    config = Config.from_env()

    assert config.token == 'bot_token'
    assert config.api_url == 'bot_api_url'
