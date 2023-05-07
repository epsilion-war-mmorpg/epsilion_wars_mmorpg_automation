from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.grinding import is_grinding_ready_state


@pytest.mark.parametrize('payload,expected', [
    ('Тюрьма /hunt_info\nВ локации можно встретить врагов.', False),
    ('❕ Информация: /hunt_info\n❓При повторном использовании бафов длительность их действия складывается.', True),
])
def test_is_hunting_ready_state(payload: str, expected: bool):
    button = Mock()
    button.text = '⚔️ Найти врагов'
    event_mock = Mock()
    event_mock.message.message = payload
    event_mock.message.button_count = 2
    event_mock.message.buttons = [[Mock(), button]]

    result = is_grinding_ready_state(event_mock)

    assert result is expected
