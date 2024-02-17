import pytest

from unittest.mock import AsyncMock

from tg_bot.src.main import handle_error


@pytest.mark.asyncio
async def test_error_handler(write_commands):
    message = AsyncMock()
    await handle_error(message)

    first_text = "Не могу понять чего Вы хотите, возможно, Вы напутали команду?🫡"
    second_text = f'Выберите одну из следующих или пришлите рентгеновский снимок:\n{write_commands}'

    assert message.reply.call_count == 1
    assert message.answer.call_count == 1

    assert message.reply.call_args_list[0][1]['text'] == first_text
    assert message.answer.call_args_list[0][1]['text'] == second_text
