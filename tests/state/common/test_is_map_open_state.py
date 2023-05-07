from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.common import is_map_open_state

success_map_message = """Ты открываешь 🗺 Карту.
Хмм, куда мы отправимся на этот раз?

 Легенда карты:
🏛 - Город
Остальное - Зоны охоты"""


@pytest.mark.parametrize('has_town, expected', [
    (True, True),
    (False, False),
])
def test_is_map_open_state(has_town: bool, expected: bool):
    button_mock = Mock()
    button_mock.text = '🏛 Карбарак' if has_town else 'Непонятная локация, не город'
    event_mock = Mock()
    event_mock.message.message = success_map_message
    event_mock.message.buttons = [[button_mock]]

    result = is_map_open_state(event_mock)

    assert result is expected

