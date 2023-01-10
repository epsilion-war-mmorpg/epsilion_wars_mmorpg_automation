from unittest.mock import Mock

from app.message_parsers.checks import is_selector_attack_direction


def test_is_selector_attack_direction_happy_path():
    button_first = Mock()
    button_first.text = 'В голову'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 2], [3, 4], [5], [button_last]]

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

    result = is_selector_attack_direction(event_mock)

    assert result is False
