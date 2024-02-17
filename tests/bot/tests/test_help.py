import pytest

from unittest.mock import AsyncMock

from tg_bot.src.main import handle_help


@pytest.mark.asyncio
async def test_handle_help(write_commands):
    """
    Проверка правильной вспомогательной информации от бота.

    :param write_commands: Строка с возможными командами и их описание.
    :return: None.
    """
    message = AsyncMock()
    await handle_help(message)

    text = 'Список допустимых команд:'

    assert message.answer.call_count == 2
    assert message.answer.call_args_list[0][1]['text'] == text
    assert message.answer.call_args_list[1][1]['text'] == write_commands
