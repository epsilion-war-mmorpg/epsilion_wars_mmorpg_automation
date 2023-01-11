from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.message_parsers.checks import is_selector_attack_direction


@pytest.mark.parametrize('payload', [
    'Ход 6\n',
    'Куда будешь бить?',
    'Куда бить?',
])
def test_is_selector_attack_direction_happy_path(payload: str):
    button_first = Mock()
    button_first.text = 'В голову'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 2], [3, 4], [5], [button_last]]
    event_mock.message.message = payload

    result = is_selector_attack_direction(event_mock)

    assert result is True


def test_is_selector_attack_direction_buttons_not_found():
    event_mock = Mock()
    event_mock.message.buttons = []

    result = is_selector_attack_direction(event_mock)

    assert result is False


def test_is_selector_attack_direction_invalid_buttons():
    button_first = Mock()
    button_first.text = 'В голову'
    button_last = Mock()
    button_last.text = 'Другой текст'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 2], [3, 4], [5], [button_last]]
    event_mock.message.message = 'Ход 10'

    result = is_selector_attack_direction(event_mock)

    assert result is False


def test_is_selector_attack_direction_invalid_original_message():
    button_first = Mock()
    button_first.text = 'В голову'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 2], [3, 4], [5], [button_last]]
    event_mock.message.message = '📍 Ты победил своего врага -  👨🏽‍🎤 Мародер 🔸10 💔'

    result = is_selector_attack_direction(event_mock)

    assert result is False


def test_is_selector_attack_direction_skip_already_ended_turn_message():
    button_first = Mock()
    button_first.text = 'В голову'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 2], [3, 4], [5], [button_last]]
    event_mock.message.message = 'Ход 10\n 🦅 Гриф 🔸9 ❤️(0/500) бьет в ноги и наносит 47'

    result = is_selector_attack_direction(event_mock)

    assert result is False
