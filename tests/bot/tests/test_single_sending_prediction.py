import pytest

from aiogram.enums import ParseMode

from tests.bot.bot_api_mock import bot_api_mock


@pytest.mark.asyncio
async def test_200_single_sending_prediction_handler(bot, mocker):
    """
    Проверка удачного предсказания.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=200,
        response=[{'severity': 2}]
    )
    caption = 'Колено на Вашей фотографии отношу к *Mild* степень остеоартрита'
    message.answer_photo.assert_called_with(photo=message.photo[-1].file_id,
                                            parse_mode=ParseMode.MARKDOWN_V2,
                                            caption=caption)


@pytest.mark.asyncio
async def test_400_single_sending_prediction_handler(bot, mocker):
    """
    Проверка предсказания, когда у пользователя что-то пошло не так.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=400,
        response={'detail': 'Not Found'}
    )
    error_message = "Получена ошибка от API:\n {'detail': 'Not Found'}"
    message.answer.assert_called_with(error_message)


@pytest.mark.asyncio
async def test_500_single_sending_prediction_handler(bot, mocker):
    """
    Проверка предсказания, когда с сервером что-то не так.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    response = 'Ошибка на сервере, повторите попытку позже'
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=500,
        response=response
    )
    message.answer.assert_called_with(response)
