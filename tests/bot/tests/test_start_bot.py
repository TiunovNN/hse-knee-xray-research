import pytest

from aiogram.types import BotCommandScopeDefault

from tg_bot.src.main import start_bot, COMMANDS


@pytest.mark.asyncio
async def test_start_bot(bot, mocker):
    mocker.patch.object(bot, 'set_my_commands', return_value=None)
    await start_bot(bot)

    bot.set_my_commands.assert_called_with(COMMANDS, BotCommandScopeDefault())
