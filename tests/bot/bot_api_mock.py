import io
import random

from unittest.mock import AsyncMock

from aiogram import Bot
from aiogram.client.session import aiohttp
from aiogram.types import PhotoSize

from tests.bot.mocked_response import MockResponse
from tg_bot.src.main import handle_single_sending_prediction, handle_save_training_image # noqa


async def bot_api_mock(
        bot: Bot,
        mocker,
        status: int,
        response,
        executable_function='handle_single_sending_prediction',
        caption=None
) -> AsyncMock:
    message = AsyncMock()

    mock_file = random.randbytes(100_000)
    mocker.patch.object(bot, 'download', return_value=io.BytesIO(mock_file))
    if caption is not None:
        message.caption = caption
    file_id = 'AgACAgIAAxkBAAIB8WXPyEi0D2XcU4exzydQTJPsyX-FAAJv2jEb0sSBSkkm5' \
              'nsplvQXAQADAgADeAADNAQ'
    mocker.patch.object(message, 'photo', return_value=[
        PhotoSize(
            file_id=file_id,
            file_unique_id='AQADb9oxG9LEgUp9',
            width=800,
            height=626,
            file_size=109618)
    ])

    fake_url = 'https://example.com'
    async with aiohttp.ClientSession(base_url=fake_url) as mocked_session:
        fake_response = MockResponse(status, response)
        mocker.patch.object(mocked_session, 'post', return_value=fake_response)

        await globals()[executable_function](message, bot, mocked_session)
        return message
