import asyncio
import io
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import catboost
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

from prediction import Predictor


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


@dp.message(CommandStart())
async def start(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        f'Привет! Этот бот может подсказать степень развития остеоартрита коленного сустава.\n'
        f'Просто отправь рентгеновский снимок'
    )


@dp.message(F.photo)
async def handle_image(message: types.Message, bot: Bot, predictor: Predictor):
    logging.info(f'{message.photo=!r}')
    buffer: io.BytesIO = await bot.download(message.photo[-1])
    start_time = time.perf_counter()
    severity = predictor.predict(buffer)
    logging.info(f'Predicted: {time.perf_counter() - start_time}')
    await message.answer(f'Степень остеоартрита: {severity}')


async def main():
    configure_logging()
    config = Config.from_env()
    bot = Bot(config.token)
    predictor = Predictor(catboost.CatBoostClassifier().load_model(config.model_path))
    await dp.start_polling(bot, predictor=predictor)


if __name__ == '__main__':
    asyncio.run(main())
