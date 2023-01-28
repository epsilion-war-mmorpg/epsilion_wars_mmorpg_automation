from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat


def test_get_buttons_flat_happy_path():
    event = Mock()
    event.message.buttons = [
        [1, 2],
        [3],
        [4, 5, 1],
    ]

    result = get_buttons_flat(event)

    assert result == [1, 2, 3, 4, 5, 1]


def test_get_buttons_flat_empty_buttons():
    event = Mock()
    event.message.buttons = []

    result = get_buttons_flat(event)

    assert result == []
