import pytest

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from unittest.mock import AsyncMock

from tests.bot.utils import TEST_USER, TEST_CHAT
from tg_bot.src.main import handle_cancel, handle_wrong_cancel, Action


@pytest.mark.asyncio
async def test_cancel_handler(storage, bot):
    message = AsyncMock()
    state = FSMContext(storage=storage, key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id))
    await state.set_state(Action.help_with_training.state)
    await handle_cancel(message, state)

    assert await state.get_state() is None
    message.answer.assert_called_with(text='Завершили /help_with_training, можете продолжать делать что хотите.😎')


@pytest.mark.asyncio
async def test_wrong_cancel_handler():
    message = AsyncMock()
    await handle_wrong_cancel(message)

    message.answer.assert_called_with(text='В данный момент не выбрана команда, которую можно отменить.')
