from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.vendor import is_random_vendor_meet

success_map_message = """👲 Странствующий торговец
Бдумс, а вот и я.
Бери пока не поздно:

🍪 Печенька - 1 шт
Пополняет счет на 1 печеньку.

/use_getcoockie"""


def test_is_random_vendor_meet():
    button_mock = Mock()
    button_mock.text = 'Покинуть торговца'
    event_mock = Mock()
    event_mock.message.message = success_map_message
    event_mock.message.buttons = [[button_mock]]

    result = is_random_vendor_meet(event_mock)

    assert result is True
