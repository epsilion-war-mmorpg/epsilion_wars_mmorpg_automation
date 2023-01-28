from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.states import is_hunting_ready_state


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('Тюрьма /hunt_info\nВ локации можно встретить врагов.', False),
    ('🎣 Рыбацкое место\n🔸 Уровень монстров: Монстров пока нет=(\nВ локации можно встретить врагов. Кто же будет следующим?', False),
    ('❕ Информация: /hunt_info\nВ локации можно встретить врагов. Кто же будет следующим?', True),
])
def test_is_hunting_ready_state(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_hunting_ready_state(event_mock)

    assert result is expected
