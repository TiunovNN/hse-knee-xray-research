import pytest

from unittest.mock import AsyncMock

from tg_bot.src.main import handle_start


@pytest.mark.asyncio
async def test_start_handler():
    """
    Проверка корректной отработки команды start

    :return: None.
    """
    message = AsyncMock()
    await handle_start(message)

    text = f'Здравствуйте, {message.from_user.full_name}! Я могу подсказать ' \
           'степень развития остеоартрита коленного сустава по его ' \
           'рентгеновскому снимку.'
    message.answer.assert_called_with(text=text)
