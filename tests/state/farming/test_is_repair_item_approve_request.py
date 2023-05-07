from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.farming import is_repair_item_approve_request


def test_is_repair_item_approve_request():
    button_mock = Mock()
    button_second_mock = Mock()
    button_mock.text = 'Отремонтировать'
    button_second_mock.text = 'Назад'
    event_mock = Mock()
    event_mock.message.message = """⚒ Кузнец Грыл

Починить 🔪 Деревянный меч [I] (19/22) за 300 💰?"""
    event_mock.message.buttons = [[button_mock, button_second_mock]]

    result = is_repair_item_approve_request(event_mock)

    assert result is True
