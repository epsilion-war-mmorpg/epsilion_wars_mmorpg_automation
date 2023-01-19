from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.parsers.checks.states import is_died_state


@pytest.mark.parametrize('button_text,expected', [
    ('Непонятная кнопка', False),
    ('💀 Принять участь', True),
])
def test_is_died_state_by_button(button_text: str, expected: bool):
    button = Mock()
    button.text = button_text
    event_mock = Mock()
    event_mock.message.message = ''
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_died_state(event_mock)

    assert result is expected


@pytest.mark.parametrize('message_text,expected', [
    ('Тебя убил: ☠️ Гигантский скелет 🔸14\n\nТы был отправлен восстанавливаться в город', True),
    ('📍  🧟‍♂️ Ник 🔸14 убивает   🧟‍♂️ ВторойНик 🔸14 💔🏵 Потеряно славы: 10\n\n Ты отправляешься в ближайший город на восстановление', True),
    ('любое другое сообщение', False),
])
def test_is_died_state_without_button(message_text: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = message_text
    event_mock.message.button_count = 0
    event_mock.message.buttons = []

    result = is_died_state(event_mock)

    assert result is expected