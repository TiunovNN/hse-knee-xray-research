import pytest
import pytest_asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tests.bot.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope='session')
async def storage():
    memory_storage = MemoryStorage()
    try:
        yield memory_storage
    finally:
        await memory_storage.close()


@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture()
def show_classes():
    return "'Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe'"


@pytest.fixture()
def write_commands():
    return '/start - Начать знакомство.\n' \
           '/help - Список команд.\n' \
           '/description - Получить описание бота.\n' \
           '/help_with_training - Загрузить рентгеновский снимок с ' \
           'известным результатом для моего улучшения ' \
           "('Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe').\n" \
           '/cancel - Отменить некоторые действия или завершить ' \
           'определенные ожидания (будет описываться дальше).'
