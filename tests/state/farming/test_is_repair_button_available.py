from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.farming import is_repair_button_available


def test_is_repair_button_available():
    button_mock = Mock()
    button_second_mock = Mock()
    button_mock.text = 'Ремонт'
    button_second_mock.text = 'jjdjdjd'
    event_mock = Mock()
    event_mock.message.message = ''
    event_mock.message.buttons = [[button_second_mock, button_mock]]

    result = is_repair_button_available(event_mock)

    assert result is True
