from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.message_parsers.checks import is_died_state


@pytest.mark.parametrize('button_text,expected', [
    ('Непонятная кнопка', False),
    ('💀 Принять участь', True),
])
def test_is_died_state(button_text: str, expected: bool):
    button = Mock()
    button.text = button_text
    event_mock = Mock()
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_died_state(event_mock)

    assert result is expected
