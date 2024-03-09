from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.action.combo_strategy import priority_strategy

skip_button = Mock()
skip_button.text = 'Пропустить'
runaway_button = Mock()
runaway_button.text = 'Сбежать'


def test_priority_strategy_happy_path(combo_priority_strategy_overloaded):
    button1_mock = Mock()
    button1_mock.text = 'Неизвестный приём (500🗡)'
    button2_mock = Mock()
    button2_mock.text = 'Внутренняя сила (2🗡; 3🛡)'
    button3_mock = Mock()
    button3_mock.text = 'По наитию (3 🥊)'
    event_mock = Mock()
    event_mock.message.buttons = [[button1_mock, button2_mock, button3_mock], [skip_button, runaway_button]]

    result = priority_strategy(event_mock)

    assert result.text == 'По наитию (3 🥊)'


def test_priority_strategy_priority_not_found(combo_priority_strategy_overloaded):
    button1_mock = Mock()
    button1_mock.text = 'Неизвестный приём №1'
    button2_mock = Mock()
    button2_mock.text = 'Неизвестный приём №2'
    event_mock = Mock()
    event_mock.message.buttons = [[button1_mock, button2_mock], [skip_button, runaway_button]]

    result = priority_strategy(event_mock)

    assert result.text == 'Неизвестный приём №1'
