import pytest

from unittest.mock import AsyncMock

from tg_bot.src.main import handle_error


@pytest.mark.asyncio
async def test_error_handler(write_commands):
    """
    Проверка правильной реакции, когда бот не понимает что от него требуется.

    :param write_commands: Строка с возможными командами и их описание.
    :return: None.
    """
    message = AsyncMock()
    await handle_error(message)

    first = "Не могу понять чего Вы хотите, возможно, Вы напутали команду?🫡"
    text = 'Выберите одну из следующих или пришлите рентгеновский снимок:\n' \
           f'{write_commands}'

    assert message.reply.call_count == 1
    assert message.answer.call_count == 1

    assert message.reply.call_args_list[0][1]['text'] == first
    assert message.answer.call_args_list[0][1]['text'] == text
