import os
import shutil
import pytest

from tg_bot.src.main import create_help_dir


@pytest.mark.asyncio
async def test_create_help_dir():
    # переходим в бота, сложная конструкция, чтобы запускать как из файла, так и из корня проекта
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/../../../tg_bot/')
    contents = os.listdir('./')

    # Print the contents
    for item in contents:
        print(item)
    help_images_path = 'help_images'
    test_help_images_path = 'test_help_images'

    # переименовываем для сохранения того, что есть локально, чтоб можно было протестировать, а затем восстановить
    if os.path.exists(help_images_path):
        os.rename(help_images_path, test_help_images_path)

    try:
        # отсутствует изначально директория для хранений
        assert not os.path.isdir(help_images_path)

        os.chdir('./src/')
        # создание директорий
        create_help_dir()
        os.chdir('./../')

        # проверка создания папок
        assert os.path.isdir(help_images_path)
        assert os.path.isdir(help_images_path + '/Normal')
        assert os.path.isdir(help_images_path + '/Doubtful')
        assert os.path.isdir(help_images_path + '/Mild')
        assert os.path.isdir(help_images_path + '/Moderate')
        assert os.path.isdir(help_images_path + '/Severe')
    finally:
        # удаление папки и подпапок и обратное переименовывание
        shutil.rmtree(help_images_path)
        if os.path.exists(test_help_images_path):
            os.rename(test_help_images_path, help_images_path)
