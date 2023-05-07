from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.farming import is_repair_item_selector


def test_is_repair_item_selector_happy_path():
    event_mock = Mock()
    event_mock.message.message = """⚒ Кузнец Аакмаан

Что хочешь отремонтировать?

❓ Каждый ремонт отнимает 1 максимальную прочность у снаряжения"""

    result = is_repair_item_selector(event_mock)

    assert result is True


def test_is_repair_item_selector_not_repairable():
    event_mock = Mock()
    event_mock.message.message = """⚒ Кузнец Грыл

Тебе не требуется ремонт"""

    result = is_repair_item_selector(event_mock)

    assert result is True
