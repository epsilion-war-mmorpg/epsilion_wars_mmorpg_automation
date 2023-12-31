from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.common import is_hp_updated_message


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('💖 Ваше здоровье полностью восстановлено', True),
    ('💖 ваше здоровье полностью восстановлено', True),
    ('💖 Ваше здоровье восстановлено на 50%', True),
    ('💗 Восстановлено 62 ед. здоровья. Текущее здоровье:  ❤️ (250/250)', True),
])
def test_is_hp_updated_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_hp_updated_message(event_mock)

    assert result is expected
