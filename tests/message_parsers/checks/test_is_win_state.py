from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.parsers.checks.states import is_win_state


@pytest.mark.parametrize('button_text,expected', [
    ('Непонятная кнопка', False),
    ('✅ Забрать нaграду', True),
    ('В зону охоты', False),
])
def test_is_win_state(button_text: str, expected: bool):
    button = Mock()
    button.text = button_text
    event_mock = Mock()
    event_mock.message.message = ''
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_win_state(event_mock)

    assert result is expected


def test_is_win_state_after_escape():
    button = Mock()
    button.text = 'В зону охоты'
    event_mock = Mock()
    event_mock.message.message = '🤴️ Fnfnf 🔸17 попытался сбежать от  🤴️ LLL 🔸17, но попытка была провалена'
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_win_state(event_mock)

    assert result is True
