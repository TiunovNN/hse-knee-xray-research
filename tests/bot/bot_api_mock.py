import io
import random
from typing import Any, Callable

from unittest.mock import AsyncMock

from aiogram import Bot
from aiogram.client.session import aiohttp
from aiogram.types import PhotoSize

from tests.bot.mocked_response import MockResponse
from tg_bot.src.main import handle_single_sending_prediction, handle_save_training_image  # noqa


async def bot_api_mock(
        bot: Bot,
        mocker,
        status: int,
        response: Any,
        executable_function: Callable = handle_single_sending_prediction,
        caption: str | None = None
) -> AsyncMock:
    """
    Функция мокающая работу бота с созданным случайно файлом,
    мокаем api запрос и сессию и возвращаем сообщение для проверки в тесте.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :param status: Какой статус ответа ожидают от мока.
    :param response: Какой ответ ожидают от мока.
    :param executable_function: Какую функцию необходимо вызвать, по умолчанию
        handle_single_sending_prediction (предсказание по фото).
    :param caption: Описание к фотографии.
    :return: AsyncMock (types.Message).
    """
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

        await executable_function(message, bot, mocked_session)
        return message
