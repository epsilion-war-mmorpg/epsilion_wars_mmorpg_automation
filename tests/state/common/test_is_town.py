from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.buttons import MAP
from epsilion_wars_mmorpg_automation.game.state.common import is_town

success_map_message = """🏛 Цирта

С тех пор как Цирта пала, жизнь вернулась на круги своя. Город выглядит потрепанным и уставшим. Жители города были измотаны и истощены долгой и неоправданной войной. Голод миновал.

 🧟‍♂Fdgdgdgd 🔸11 ❤️(234/1234)
👥 Героев в городе: 43
☄️ Событие: ➕ Бонус опыт (+15%)

❓ Щит дает дополнительную точку блока.

Общий чат (https://t.me/epsilion_chat) | Торговый чат (https://t.me/epsilion_trade) | Новости (https://t.me/epsilion_news)"""


@pytest.mark.parametrize('has_map_button, expected', [
    (True, True),
    (False, False),
])
def test_is_town(has_map_button: bool, expected: bool):
    button_mock = Mock()
    button_mock.text = MAP if has_map_button else 'Непонятная кнопка'
    event_mock = Mock()
    event_mock.message.message = success_map_message
    event_mock.message.buttons = [[button_mock]]

    result = is_town(event_mock)

    assert result is expected

