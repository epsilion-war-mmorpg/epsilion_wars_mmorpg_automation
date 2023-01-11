from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.message_parsers.checks import is_hp_full_message


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('💖 Ваше здоровье полностью восстановлено', True),
])
def test_is_hp_full_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_hp_full_message(event_mock)

    assert result is expected
