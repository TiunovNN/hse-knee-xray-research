import asyncio
import io
import logging
import os
import sys
from dataclasses import dataclass
from http import HTTPStatus
from pprint import pformat

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import FormData
from aiohttp.client import ClientSession

CLASSES = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']
SHOW_CLASSES = ', '.join(map(repr, CLASSES))


# states
class Action(StatesGroup):
    help_with_training = State()


# Commands
COMMANDS = [
    BotCommand(
        command='start',
        description='Начать знакомство.'
    ),
    BotCommand(
        command='help',
        description='Список команд.'
    ),
    BotCommand(
        command='description',
        description='Получить описание бота.'
    ),
    BotCommand(
        command='help_with_training',
        description=f'Загрузить рентгеновский снимок с известным результатом для моего улучшения ({SHOW_CLASSES}).'
    ),
    BotCommand(
        command='cancel',
        description='Отменить некоторые действия или завершить определенные ожидания (будет описываться дальше).'
    )
]


# show commands for people
def write_commands():
    text = []
    for command in COMMANDS:
        text.append(f'/{command.command} - {command.description}')
    return '\n'.join(text)


@dataclass
class Config:
    token: str
    api_url: str

    @classmethod
    def from_env(cls) -> 'Config':
        token = os.getenv('BOT_TOKEN')
        if not token:
            raise ValueError('Please, set BOT_TOKEN')

        api_url = os.getenv('BOT_API_URL')
        if not api_url:
            raise ValueError('Please, set BOT_API_URL')

        return Config(token, api_url)


def configure_logging():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s',
        stream=sys.stdout,
        force=True,
    )


dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """
    Функция, которая откликается на команду /start, приветствует и даёт краткую информацию о боте.

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    text = f'Здравствуйте, {message.from_user.full_name}! Я могу подсказать степень развития остеоартрита коленного ' \
           'сустава по его рентгеновскому снимку.'
    await message.answer(text=text)


@dp.message(Command('help'))
async def handle_help(message: types.Message):
    """
    Функция, которая откликается на команду /help, предоставляет список доступных команд с их кратким описанием.

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    await message.answer(text='Список допустимых команд:')
    await message.answer(text=write_commands())


@dp.message(Command('description'))
async def handle_description(message: types.Message):
    """
    Функция, которая откликается на команду /description, дает более подробную информацию о нашем боте.

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    text = 'Я могу определить состояние здоровья вашего коленного сустава. Мне просто нужно прислать рентген вашего ' \
           'колена, и в ответ я скажу вам, все ли у вас в порядке или насколько всё плохо. Я могу разделить на 5 ' \
           f'классов: нормальный, сомнительный, легкий, среднетяжелый, тяжелый ({SHOW_CLASSES}). У меня есть доступ ' \
           'к модели, которая была обучена на более чем 1500 рентгеновских снимках суставов колен с разной степенью ' \
           'остеоартрита, в том числе здоровых, которые изначально были разделены на классы опытными специалистами в ' \
           'этой области.'
    await message.answer(text=text)


@dp.message(Command('help_with_training'))
async def handle_help(message: types.Message, state: FSMContext):
    """
    Функция, которая откликается на команду /help_with_training, устанавливает состояние на получение изображения и его
    класса для дальнейшего обучения.

    @param message: Объект сообщения пользователя.
    @param state: Состояние устанавливаемое внутри метода.
    @return: None.
    """
    text = 'Пожалуйста, пришлите в одном сообщении вашу фотографию рентгеновского снимка колена и к какому типу ' \
           f'относится (возможные варианты: {SHOW_CLASSES}). Если передумали или больше нечего отправить, то ' \
           'пришлите /cancel.'
    await message.answer(text=text)
    await state.set_state(Action.help_with_training.state)


@dp.message(StateFilter(Action.help_with_training), Command('cancel'))
async def handle_cancel(message: types.Message, state: FSMContext):
    """
    Функция, которая откликается на команду /cancel, убирает любое состояние и сообщает о том, какое было убрано.

    @param message: Объект сообщения пользователя.
    @param state: Состояние, которое сообщается пользователю и убирается внутри метода.
    @return: None.
    """
    st = str(await state.get_state()).split(":")[1]
    await state.clear()
    await message.answer(text=f'Завершили /{st}, можете продолжать делать что хотите.😎')


@dp.message(StateFilter(None), Command('cancel'))
async def handle_wrong_cancel(message: types.Message):
    """
    Функция, которая откликается на команду /cancel, обрабатывает отсутствие какого-либо состояния и сообщает об этом.

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    await message.answer(text='В данный момент не выбрана команда, которую можно отменить.')


@dp.message(StateFilter(None), F.photo)
async def handle_single_sending_prediction(message: types.Message, bot: Bot,
                                           httpclient: ClientSession):
    """
    Функция для состояния predict, которая обрабатывает полученные фотографии моделью и даёт предсказания, но
    прекращает свою работу после первого сообщения.

    @param message: Объект сообщения пользователя.
    @param bot: Бот для получения изображения и его передачи в модель.
    @param httpclient: Клиент для запросов к API
    @return: None.
    """
    buffer: io.BytesIO = await bot.download(message.photo[-1])
    form_data = FormData()
    form_data.add_field('files', buffer)

    async with httpclient.post('/predict', data=form_data) as response:
        if response.status == HTTPStatus.OK:
            answer = await response.json()
            severity = answer[0]['severity']
            await message.answer_photo(photo=message.photo[-1].file_id,
                                       parse_mode=ParseMode.MARKDOWN_V2,
                                       caption=f'Колено на Вашей фотографии отношу к *{CLASSES[severity]}* степень остеоартрита')
        if 400 <= response.status < 500:
            answer = await response.json()
            await message.answer(f'Получена ошибка от API:\n {pformat(answer)}')

        if response.status >= 500:
            await message.answer(f'Ошибка на сервере, повторите попытку позже')


@dp.message(StateFilter(Action.help_with_training), F.photo, F.caption.in_(CLASSES))
async def handle_save_training_image(message: types.Message, bot: Bot, httpclient: ClientSession):
    """
    Функция для состояния help_with_training, которая сохраняет изображения и информацию о том к какому классу надо
    отнести эту фотографию.

    @param message: Объект сообщения пользователя.
    @param bot: Бот для получения изображения и его сохранения.
    @return: None.
    """
    buffer: io.BytesIO = await bot.download(message.photo[-1])
    form_data = FormData()
    form_data.add_field('file', buffer)

    severity = CLASSES.index(message.caption)
    async with httpclient.post(f'/train/{severity}', data=form_data) as response:
        if response.status == HTTPStatus.OK:
            await message.answer_photo(photo=message.photo[-1].file_id,
                                       parse_mode=ParseMode.MARKDOWN_V2,
                                       caption=f'Спасибо, мы сохранили вашу фотографию класса *{message.caption}*')

        if 400 <= response.status < 500:
            answer = await response.json()
            await message.answer(f'Получена ошибка от API:\n {pformat(answer)}')

        if response.status >= 500:
            await message.answer(f'Ошибка на сервере, повторите попытку позже')


@dp.message(StateFilter(Action.help_with_training))
async def handle_wrong_save_training_image(message: types.Message):
    """
    Функция для любого состояния, которая сообщает о том, что пользователь забыл прислать фото или сообщение
    (знаем о состоянии, но не понимаем как правильно обработать обращение).

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    await message.reply(
        text='Вы забыли прислать фотографию или написать к какому классу относится, возможно неверно '
             'написали класс или прикрепили сразу несколько фотографий.')


@dp.message()
async def handle_error(message: types.Message):
    """
    Функция для любого сообщения, которое мы не смогли подчинить другим запросам, сообщаем пользователю об этом и
    предоставляем список допустимых команд.

    @param message: Объект сообщения пользователя.
    @return: None.
    """
    await message.reply(
        text="Не могу понять чего Вы хотите, возможно, Вы напутали команду?🫡")  # it's ok, it's emoji
    await message.answer(
        text=f'Выберите одну из следующих или пришлите рентгеновский снимок:\n{write_commands()}')


async def start_bot(bot: Bot):
    await bot.set_my_commands(COMMANDS, BotCommandScopeDefault())


def create_help_dir():
    help_images_path = './../help_images'
    if not os.path.exists(help_images_path):
        os.makedirs(help_images_path)
    for help_image_class in CLASSES:
        if not os.path.exists(help_images_path + '/' + help_image_class):
            os.makedirs(help_images_path + '/' + help_image_class)


async def main():
    create_help_dir()
    configure_logging()
    config = Config.from_env()
    bot = Bot(config.token)
    session = ClientSession(base_url=config.api_url)
    dp.startup.register(start_bot)
    async with session as aiohttp_client:
        await dp.start_polling(bot, httpclient=aiohttp_client, close_bot_session=True)


if __name__ == '__main__':
    asyncio.run(main())
