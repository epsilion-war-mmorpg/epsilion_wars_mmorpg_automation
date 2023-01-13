from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.parsers.checks.states import is_selector_combo


def test_is_selector_combo_happy_path():
    button_first = Mock()
    button_first.text = 'Суперудар!'
    button_invalid = Mock()
    button_invalid.text = 'Пропустить'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first], [button_invalid], [button_last]]
    event_mock.message.message = ''

    result = is_selector_combo(event_mock)

    assert result is True


def test_is_selector_combo_buttons_not_found():
    event_mock = Mock()
    event_mock.message.buttons = [[1, 2]]

    result = is_selector_combo(event_mock)

    assert result is False


def test_is_selector_combo_invalid_buttons():
    button_first = Mock()
    button_first.text = 'Суперудар!'
    button_invalid = Mock()
    button_invalid.text = 'Другой текст'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first, 1, 3], [button_invalid], [button_last]]
    event_mock.message.message = ''

    result = is_selector_combo(event_mock)

    assert result is False


def test_is_selector_combo_already_ended_battle():
    button_first = Mock()
    button_first.text = 'Суперудар!'
    button_invalid = Mock()
    button_invalid.text = 'Пропустить'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.message.buttons = [[button_first], [button_invalid], [button_last]]
    event_mock.message.message = 'Ход (0/899)'

    result = is_selector_combo(event_mock)

    assert result is False
