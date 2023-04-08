from unittest.mock import AsyncMock, Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.common import is_character_equip_select
from epsilion_wars_mmorpg_automation.game.state.grinding import is_battle_start_message

success_equip_message = """
☄️ 🧝‍♂Дикость 🔸20 ❤️(1405/1330)

Надетая экипировка:

🔪 Оружие: Чекан [III] +1 (20/30)
🎩 Шлем: Темный бацинет [III] +1 (20/30)
🎽 Доспех: Черный нагрудник [III] +1 (20/30)
🧤 Перчатки: Кровавые браслеты [III] +1 (20/30)
🥾 Сапоги: Сандали прозрения [III] +1 (20/30)
🛡 Щит: Бронзовый калкан [III] +1 (20/30)
💍 Кольцо: Печать палача [III] +1 (20/30)
📿 Колье: Янтарное ожерелье [III] +1 (20/30)
🌂 Аксессуар: -
"""


def test_is_character_equip_select_buttons_not_found():
    button = AsyncMock()
    button.text = 'second'
    event_mock = Mock()
    event_mock.message.message = success_equip_message
    event_mock.message.buttons = [[button]]

    result = is_character_equip_select(event_mock)

    assert result is False


def test_is_character_equip_select_happy_path():
    button = AsyncMock()
    button.text = '🗡 Оружие (9)'
    event_mock = Mock()
    event_mock.message.message = success_equip_message
    event_mock.message.buttons = [[button]]

    result = is_character_equip_select(event_mock)

    assert result is True
