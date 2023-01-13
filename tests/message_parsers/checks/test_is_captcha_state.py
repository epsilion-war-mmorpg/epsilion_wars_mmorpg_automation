from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.parsers.checks.messages import is_captcha_message


@pytest.mark.parametrize('payload,expected', [
    ('❕ Информация: /hunt_info\nВ локации можно встретить врагов. Кто же будет следующим?', False),
    ('На пути ты встретил капчу.\n 6 умнож. нa 6 - Нaпишите ответ числом.', True),
])
def test_is_captcha_state(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_captcha_message(event_mock)

    assert result is expected
