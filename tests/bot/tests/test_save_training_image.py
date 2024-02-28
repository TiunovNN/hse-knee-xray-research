import pytest

from aiogram.enums import ParseMode
from unittest.mock import AsyncMock

from tests.bot.bot_api_mock import bot_api_mock
from tg_bot.src.main import handle_wrong_save_training_image, handle_save_training_image


@pytest.mark.asyncio
async def test_200_save_training_image_handler(bot, mocker):
    """
    Проверка удачной помощи нам.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=200,
        response=[{'severity': 4}],
        executable_function=handle_save_training_image,
        caption='Severe'
    )
    caption = 'Спасибо, мы сохранили вашу фотографию класса *Severe*'
    message.answer_photo.assert_called_with(photo=message.photo[-1].file_id,
                                            parse_mode=ParseMode.MARKDOWN_V2,
                                            caption=caption)


@pytest.mark.asyncio
async def test_400_save_training_image_handler(bot, mocker):
    """
    Проверка помощи нам, когда у пользователя что-то пошло не так.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=400,
        response={'detail': 'Not Found'},
        executable_function=handle_save_training_image,
        caption='Severe'
    )
    error_message = "Получена ошибка от API:\n {'detail': 'Not Found'}"
    message.answer.assert_called_with(error_message)


@pytest.mark.asyncio
async def test_500_save_training_image_handler(bot, mocker):
    """
    Проверка помощи нам, когда с сервером что-то не так.

    :param bot: Мок бота.
    :param mocker: Мокер для объектов и их результатов функций.
    :return: None.
    """
    response = 'Ошибка на сервере, повторите попытку позже'
    message = await bot_api_mock(
        bot=bot,
        mocker=mocker,
        status=500,
        response=response,
        executable_function=handle_save_training_image,
        caption='Severe'
    )
    message.answer.assert_called_with(response)


@pytest.mark.asyncio
async def test_wrong_save_training_image_handler():
    """
    Проверка неудачной отправки помощи нам.

    :return: None.
    """
    message = AsyncMock()
    await handle_wrong_save_training_image(message)

    text = 'Вы забыли прислать фотографию или написать к какому классу ' \
           'относится, возможно неверно написали класс или прикрепили сразу ' \
           'несколько фотографий.'
    message.reply.assert_called_with(text=text)
