import pytest

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from unittest.mock import AsyncMock

from tests.bot.utils import TEST_USER, TEST_CHAT
from tg_bot.src.main import handle_cancel, handle_wrong_cancel, Action


@pytest.mark.asyncio
async def test_cancel_handler(storage, bot):
    """
    Проверка отчистки состояния и отправки сообщения об этом.

    :param storage: Хранилище состояний.
    :param bot: Мок бота.
    :return: None.
    """
    message = AsyncMock()
    key = StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id)
    state = FSMContext(storage=storage, key=key)

    await state.set_state(Action.help_with_training.state)
    assert await state.get_state() == Action.help_with_training.state

    await handle_cancel(message, state)

    assert await state.get_state() is None
    t = 'Завершили /help_with_training, можете продолжать делать что хотите.😎'
    message.answer.assert_called_with(text=t)


@pytest.mark.asyncio
async def test_wrong_cancel_handler():
    """
    Проверка отчистки состояния, если его нет.

    :return: None.
    """
    message = AsyncMock()
    await handle_wrong_cancel(message)

    text = 'В данный момент не выбрана команда, которую можно отменить.'
    message.answer.assert_called_with(text=text)
