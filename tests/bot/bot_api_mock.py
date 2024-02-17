import io
import random

from unittest.mock import AsyncMock

from aiogram.client.session import aiohttp
from aiogram.types import PhotoSize

from tests.bot.mocked_response import MockResponse
# следующая строка необходима
from tg_bot.src.main import handle_single_sending_prediction, handle_save_training_image


async def bot_api_mock(bot, mocker, status, response, executable_function='handle_single_sending_prediction', caption=None):
    message = AsyncMock()

    mock_file = random.randbytes(100_000)
    mocker.patch.object(bot, 'download', return_value=io.BytesIO(mock_file))
    if caption is not None:
        message.caption = caption
    mocker.patch.object(message, 'photo', return_value=[
        PhotoSize(file_id='AgACAgIAAxkBAAIB8WXPyEi0D2XcU4exzydQTJPsyX-FAAJv2jEb0sSBSkkm5nsplvQXAQADAgADeAADNAQ',
                  file_unique_id='AQADb9oxG9LEgUp9',
                  width=800,
                  height=626,
                  file_size=109618)
    ])

    async with aiohttp.ClientSession(base_url='https://example.com') as mocked_session:
        mocker.patch.object(mocked_session, 'post', return_value=MockResponse(status, response))

        await globals()[executable_function](message, bot, mocked_session)
        return message
