import pytest

from unittest.mock import AsyncMock

from tg_bot.src.main import handle_description


@pytest.mark.asyncio
async def test_handle_description(show_classes):
    """
    Проверка отправки описания.

    :param show_classes: Строка с возможными классами.
    :return: None.
    """
    message = AsyncMock()
    await handle_description(message)

    text = 'Я могу определить состояние здоровья вашего коленного сустава. ' \
           'Мне просто нужно прислать рентген вашего колена, и в ответ я ' \
           'скажу вам, все ли у вас в порядке или насколько всё плохо. Я ' \
           'могу разделить на 5 классов: нормальный, сомнительный, легкий, ' \
           f'среднетяжелый, тяжелый ({show_classes}). У меня есть доступ к ' \
           'модели, которая была обучена на более чем 1500 рентгеновских ' \
           'снимках суставов колен с разной степенью остеоартрита, в том ' \
           'числе здоровых, которые изначально были разделены на классы ' \
           'опытными специалистами в этой области.'
    message.answer.assert_called_with(text=text)
