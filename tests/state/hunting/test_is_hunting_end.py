from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.hunting import is_hunting_end


def test_is_hunting_end_happy_path():
    button = AsyncMock()
    button.text = 'Вернуться в локацию'
    event_mock = Mock()
    event_mock.message.message = """🏹 Охота завершена, ты добыл:

✨ Опыта: 192
▫️ Опыта охоты: 100

🥩 Кусок мяса
🥩 Кусок мяса
🦴 Кость
🥩 Кусок мяса"""
    event_mock.message.buttons = [[button]]

    result = is_hunting_end(event_mock)

    assert result is True


def test_is_hunting_end_without_buttons():
    event_mock = Mock()
    event_mock.message.message = """🏹 Охота сегодня была особенно удачна, удалось поймать много дичи:

✨ Опыта: 1280
▫️ Опыта охоты: 400

🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🦴 Кость
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса
🥩 Кусок мяса"""
    event_mock.message.buttons = []

    result = is_hunting_end(event_mock)

    assert result is True
