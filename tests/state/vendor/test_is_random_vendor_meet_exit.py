from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.vendor import is_random_vendor_meet_exit


def test_is_random_vendor_meet_exit_skip():
    button_mock = Mock()
    button_mock.text = 'Войти в город'
    event_mock = Mock()
    event_mock.message.message = "Ты покинул 👲 Странствующего торговца"
    event_mock.message.buttons = [[button_mock]]

    result = is_random_vendor_meet_exit(event_mock)

    assert result is True


def test_is_random_vendor_meet_exit_after_buy():
    button_mock = Mock()
    button_mock.text = 'Войти в город'
    event_mock = Mock()
    event_mock.message.message = "Ты успешно купил - 🍪 Печенька"
    event_mock.message.buttons = [[button_mock]]

    result = is_random_vendor_meet_exit(event_mock)

    assert result is True
