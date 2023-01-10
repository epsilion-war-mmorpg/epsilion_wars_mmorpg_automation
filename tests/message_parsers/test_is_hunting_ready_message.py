from unittest.mock import Mock

import pytest

from app.message_parsers.checks import is_hunting_ready_message


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('❕ Информация: /hunt_info\nВ локации можно встретить врагов. Кто же будет следующим?', True),
])
def test_is_hunting_ready_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_hunting_ready_message(event_mock)

    assert result is expected
