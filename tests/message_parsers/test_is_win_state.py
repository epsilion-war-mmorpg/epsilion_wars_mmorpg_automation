from unittest.mock import Mock

import pytest

from app.message_parsers.checks import is_win_state


@pytest.mark.parametrize('button_text,expected', [
    ('Непонятная кнопка', False),
    ('✅ Забрать нaграду', True),
])
def test_is_win_state(button_text: str, expected: bool):
    button = Mock()
    button.text = button_text
    event_mock = Mock()
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_win_state(event_mock)

    assert result is expected
