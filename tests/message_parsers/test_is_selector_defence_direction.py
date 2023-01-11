from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.message_parsers.checks import is_selector_defence_direction


@pytest.mark.parametrize('payload,expected', [
    ('Другое сообщение', False),
    ('Что будешь блокировать?', True),
])
def test_is_selector_defence_direction(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_selector_defence_direction(event_mock)

    assert result is expected
