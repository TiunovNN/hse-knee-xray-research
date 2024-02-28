import pytest

from aiogram.types import BotCommandScopeDefault

from tg_bot.src.main import start_bot, COMMANDS


@pytest.mark.asyncio
async def test_start_bot(bot, mocker):
    """
    Проверка удачного старта бота с необходимыми командами.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    mocker.patch.object(bot, 'set_my_commands', return_value=None)
    await start_bot(bot)

    bot.set_my_commands.assert_called_with(COMMANDS, BotCommandScopeDefault())
