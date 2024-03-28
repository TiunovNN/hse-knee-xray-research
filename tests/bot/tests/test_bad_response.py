import pytest

from tests.bot.mocked_response import MockResponse
from tg_bot.src.main import bad_response
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_400_bad_response(bot):
    """
    Проверка предсказания, когда у пользователя что-то пошло не так.

    :param bot: Мок бота.
    :return: None.
    """
    message = AsyncMock()
    await bad_response(MockResponse(400, {'detail': 'Not Found'}), message)
    error_message = "Получена ошибка от API:\n {'detail': 'Not Found'}"
    message.answer.assert_called_with(error_message)


@pytest.mark.asyncio
async def test_500_bad_response(bot):
    """
    Проверка предсказания, когда с сервером что-то не так.

    :param bot: Мок бота.
    :return: None.
    """
    message = AsyncMock()
    response = 'Ошибка на сервере, повторите попытку позже'
    await bad_response(MockResponse(500, response), message)
    message.answer.assert_called_with(response)
