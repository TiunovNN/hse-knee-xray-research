import asyncio
import io
import logging
import os
import sys
import time
import catboost

from dataclasses import dataclass
from pathlib import Path
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BotCommand, BotCommandScopeDefault

from prediction import Predictor


CLASSES = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']
SHOW_CLASSES = '"' + '", "'.join(CLASSES[:-1]) + f'" or "{CLASSES[-1]}"'


# states
class Action(StatesGroup):
    predict = State()
    help_with_training = State()
    lots_of_predictions = State()


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
        command='predict',
        description='Предсказать результат состояния колена по рентгеновс(ому/им) снимк(у/ам).'
    ),
    BotCommand(
        command='lots_of_predictions',
        description='Непрерывно предсказывать по рентгеновским снимкам колен.'
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
    model_path: str

    @classmethod
    def from_env(cls) -> 'Config':
        token = os.getenv('BOT_TOKEN')
        if not token:
            raise ValueError('Please, set BOT_TOKEN')

        model_path = os.getenv('BOT_MODEL_PATH')
        if not model_path:
            raise ValueError('Please, set BOT_MODEL_PATH')

        if not Path(model_path).is_file():
            raise ValueError(f'File {model_path} does not exist')

        return Config(token, model_path)


def configure_logging():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s',
        stream=sys.stdout,
        force=True,
    )


dp = Dispatcher()

# Commands
# /start
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    text = f'Здравствуйте, {message.from_user.full_name}! Я могу подсказать степень развития остеоартрита коленного ' \
           'сустава по его рентгеновскому снимку.'
    await message.answer(text=text)


# /help
@dp.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(text='Список допустимых команд:')
    await message.answer(text=write_commands())


# /description
@dp.message(Command('description'))
async def handle_description(message: types.Message):
    text = 'Я могу определить состояние здоровья вашего коленного сустава. Мне просто нужно прислать рентген вашего ' \
           'колена, и в ответ я скажу вам, все ли у вас в порядке или насколько всё плохо. Я могу разделить на 5 ' \
           f'классов: нормальный, сомнительный, легкий, среднетяжелый, тяжелый ({SHOW_CLASSES}). У меня есть доступ ' \
           'к модели, которая была обучена на более чем 1500 рентгеновских снимках суставов колен с разной степенью ' \
           'остеоартрита, в том числе здоровых, которые изначально были разделены на классы опытными специалистами в ' \
           'этой области.'
    await message.answer(text=text)


# /predict
@dp.message(Command('predict'))
async def handle_predict(message: types.Message, state: FSMContext):
    text = 'Пожалйуста, пришлите фотографию рентгеновского снимка вашего колена, если передумали, то отправьте /cancel.'
    await message.answer(text=text)
    await state.set_state(Action.predict.state)


# lots_of_predictions
@dp.message(Command('lots_of_predictions'))
async def handle_lots_of_predictions(message: types.Message, state: FSMContext):
    text = 'Пожалйуста, пришлите фотографии рентгеновских снимков колен, если передумали или больше не хотите ничего ' \
           'отправлять, то пришлите команду /cancel.'
    await message.answer(text=text)
    await state.set_state(Action.lots_of_predictions.state)


# help_with_training
@dp.message(Command('help_with_training'))
async def handle_help(message: types.Message, state: FSMContext):
    text = 'Пожалуйста, пришлите в одном сообщении вашу фотографию рентгеновского снимка колена и к какому типу ' \
           f'относится (возможные варианты: {SHOW_CLASSES}). Если передумали или больше нечего отправить, то ' \
           'пришлите /cancel.'
    await message.answer(text=text)
    await state.set_state(Action.help_with_training.state)


# cancel
@dp.message(StateFilter(Action.predict), Command('cancel'))
@dp.message(StateFilter(Action.help_with_training), Command('cancel'))
@dp.message(StateFilter(Action.lots_of_predictions), Command('cancel'))
async def handle_cancel(message: types.Message, state: FSMContext):
    st = str(await state.get_state()).split(":")[1]
    await state.clear()
    await message.answer(text=f'Завершили /{st}, можете продолжать делать что хотите.😎')


# wrong cancel
@dp.message(StateFilter(None), Command('cancel'))
async def handle_wrong_cancel(message: types.Message):
    await message.answer(text='В данный момент не выбрана команда, которую можно отменить.')


# Helping methods
# unstoppable prediction
@dp.message(StateFilter(Action.lots_of_predictions), F.photo)
async def handle_unstoppable_prediction(message: types.Message, bot: Bot, predictor: Predictor):
    logging.info(f'{message.photo=!r}')
    buffer: io.BytesIO = await bot.download(message.photo[-1])
    start_time = time.perf_counter()
    severity = predictor.predict(buffer)
    logging.info(f'Predicted: {time.perf_counter() - start_time}')
    await message.answer_photo(photo=message.photo[-1].file_id, parse_mode=ParseMode.MARKDOWN_V2,
                               caption=f'Колено на Вашей фотографии отношу к *{CLASSES[severity]}* степень остеоартрита')


# single sending prediction
@dp.message(StateFilter(Action.predict), F.photo)
async def handle_single_sending_prediction(message: types.Message, state: FSMContext, bot: Bot, predictor: Predictor):
    await handle_unstoppable_prediction(message, bot, predictor)
    await state.clear()


# save training image
@dp.message(StateFilter(Action.help_with_training), F.photo, F.caption.in_(CLASSES))
async def handle_save_training_image(message: types.Message, bot: Bot):
    photo_path = f'./../help_images/{message.caption}/{message.photo[-1].file_id}.jpg'
    await bot.download(message.photo[-1], destination=photo_path)
    await message.answer_photo(photo=message.photo[-1].file_id, parse_mode=ParseMode.MARKDOWN_V2,
                               caption=f'Спасибо, мы сохранили вашу фотографию класса *{message.caption}*')


# wrong save training image
@dp.message(StateFilter(Action.predict))
@dp.message(StateFilter(Action.lots_of_predictions))
@dp.message(StateFilter(Action.help_with_training))
async def handle_wrong_save_training_image(message: types.Message):
    await message.reply(text='Вы забыли прислать фотографию или написать к какому классу относится, возможно неверно '
                             'написали класс или прикрепили сразу несколько фотографий.')


# wrong photo state
@dp.message(F.photo)
async def handle_wrong_photo_state(message: types.Message):
    await message.answer(text='Если вы хотите получить предсказание, то пропишите /predict.\nДля получения '
                              'предсказания для каждого нового сообщения с фотографией, тогда /lots_of_predictions.\n'
                              'Для помощи в моём обучении используй /help_with_training.')


# /other_messages
@dp.message()
async def handle_error(message: types.Message):
    await message.reply(text="Не могу понять чего вы хотите, возможно, вы напутали команду?🫡")  # it's ok, it's emoji
    await message.answer(text=f'Выберите одну из следующих:\n{write_commands()}')


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
    predictor = Predictor(catboost.CatBoostClassifier().load_model(config.model_path))
    dp.startup.register(start_bot)
    try:
        await dp.start_polling(bot, predictor=predictor)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
