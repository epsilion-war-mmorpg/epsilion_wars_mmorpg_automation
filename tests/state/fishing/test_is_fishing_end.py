from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.fishing import is_fishing_end


def test_is_fishing_end_happy_path():
    button = AsyncMock()
    button.text = 'Вернуться в локацию'
    event_mock = Mock()
    event_mock.message.message = """🎣️ Рыбалка завершена, ты поймал:

✨ Опыта: 123
▫️ Опыта рыбалки: 112

🐟 Карбарась
🌿 Водоросли"""
    event_mock.message.buttons = [[button]]

    result = is_fishing_end(event_mock)

    assert result is True
