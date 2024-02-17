import pytest

from aiogram.enums import ParseMode

from tests.bot.bot_api_mock import bot_api_mock


@pytest.mark.asyncio
async def test_200_single_sending_prediction_handler(bot, mocker):
    message = await bot_api_mock(bot, mocker, 200, [{'severity': 2}])
    message.answer_photo.assert_called_with(photo=message.photo[-1].file_id,
                                            parse_mode=ParseMode.MARKDOWN_V2,
                                            caption=f'Колено на Вашей фотографии отношу к *Mild* степень остеоартрита')


@pytest.mark.asyncio
async def test_400_single_sending_prediction_handler(bot, mocker):
    message = await bot_api_mock(bot, mocker, 400, {'detail': 'Not Found'})
    message.answer.assert_called_with("Получена ошибка от API:\n {'detail': 'Not Found'}")


@pytest.mark.asyncio
async def test_500_single_sending_prediction_handler(bot, mocker):
    response = 'Ошибка на сервере, повторите попытку позже'
    message = await bot_api_mock(bot, mocker, 500, response)
    message.answer.assert_called_with(response)
