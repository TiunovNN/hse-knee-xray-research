import pytest

from aiogram.enums import ParseMode
from unittest.mock import AsyncMock

from tests.bot.bot_api_mock import bot_api_mock
from tg_bot.src.main import handle_wrong_save_training_image


@pytest.mark.asyncio
async def test_200_save_training_image_handler(bot, mocker):
    message = await bot_api_mock(bot, mocker, 200, [{'severity': 4}], executable_function='handle_save_training_image', caption='Severe')
    message.answer_photo.assert_called_with(photo=message.photo[-1].file_id,
                                            parse_mode=ParseMode.MARKDOWN_V2,
                                            caption=f'Спасибо, мы сохранили вашу фотографию класса *Severe*')


@pytest.mark.asyncio
async def test_400_save_training_image_handler(bot, mocker):
    message = await bot_api_mock(bot, mocker, 400, {'detail': 'Not Found'}, executable_function='handle_save_training_image', caption='Severe')
    message.answer.assert_called_with("Получена ошибка от API:\n {'detail': 'Not Found'}")


@pytest.mark.asyncio
async def test_500_save_training_image_handler(bot, mocker):
    response = 'Ошибка на сервере, повторите попытку позже'
    message = await bot_api_mock(bot, mocker, 500, response, executable_function='handle_save_training_image', caption='Severe')
    message.answer.assert_called_with(response)


@pytest.mark.asyncio
async def test_wrong_save_training_image_handler():
    message = AsyncMock()
    await handle_wrong_save_training_image(message)

    text = 'Вы забыли прислать фотографию или написать к какому классу относится, возможно неверно написали класс ' \
           'или прикрепили сразу несколько фотографий.'
    message.reply.assert_called_with(text=text)
