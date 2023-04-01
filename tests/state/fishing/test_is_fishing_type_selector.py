from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.fishing import is_fishing_type_selector


def test_is_fishing_type_selector_happy_path():
    button_rod = AsyncMock()
    button_rod.text = '🎣 Рыбачить 10 минут - 🔋 1'
    button_return = AsyncMock()
    button_return.text = '🎣 Рыбачить 30 минут - 🔋 3'

    event_mock = Mock()
    event_mock.message.message = '🎣 рыбалка  в некоторых водоемах можно рыбачить рыбу  ❓ если закончить рыбалку раньше времени, прочность удочки уменьшится, а награда не соберется.'
    event_mock.message.buttons = [[button_rod, button_return]]

    result = is_fishing_type_selector(event_mock)

    assert result is True
