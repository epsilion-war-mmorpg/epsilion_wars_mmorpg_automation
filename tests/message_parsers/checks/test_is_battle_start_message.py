from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.messages import is_battle_start_message


@pytest.mark.parametrize('payload,expected', [
    ('❕ Информация: /hunt_info\nВ локации можно встретить врагов. Кто же будет следующим?', False),
    ('Вот ты и встретил своего врага.\n\nТвоим соперником будет 💀 Скелет в доспехах 🔸14 ❤️(650/650).', True),
])
def test_is_battle_start_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_battle_start_message(event_mock)

    assert result is expected
