import pytest

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from unittest.mock import AsyncMock

from tests.bot.utils import TEST_USER, TEST_CHAT
from tg_bot.src.main import handle_help_us, Action


@pytest.mark.asyncio
async def test_help_us_handler(storage, bot, show_classes):
    """
    Проверка изменения состояния и отправки сообщения при желании помочь нам.

    :param storage: Хранилище состояний.
    :param bot: Мок бота.
    :param show_classes: Строка с возможными классами.
    :return: None.
    """
    message = AsyncMock()
    key = StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id)
    state = FSMContext(storage=storage, key=key)
    await handle_help_us(message, state)

    text = 'Пожалуйста, пришлите в одном сообщении вашу фотографию ' \
           'рентгеновского снимка колена и к какому типу относится ' \
           f'(возможные варианты: {show_classes}). Если передумали ' \
           'или больше нечего отправить, то пришлите /cancel.'
    message.answer.assert_called_with(text=text)
    assert await state.get_state() == Action.help_with_training.state
