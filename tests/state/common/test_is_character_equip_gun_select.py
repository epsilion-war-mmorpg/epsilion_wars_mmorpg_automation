from unittest.mock import Mock, AsyncMock

from epsilion_wars_mmorpg_automation.game.state.common import is_character_equip_gun_select

success_equip_message = """
☄️ 🧝‍♂Дикость 🔸20 ❤️(1405/1330)

Надетая экипировка:

🔪 Оружие: Удочка ученика [I] 
🎩 Шлем: Забрало из бронзы [II] +1
🎽 Доспех: Пробитая кольчуга [II] +1
🧤 Перчатки: Строгие перчатки [II] +1
🥾 Сапоги: Стальные боты [II] +1
🛡 Щит: Потертая тарга [II] +1
💍 Кольцо: Перстень здравия [II] 
📿 Колье: Колье стараний [II] 
🌂 Аксессуар: -
"""


def test_is_character_equip_gun_select_buttons_not_found():
    event_mock = Mock()
    event_mock.message.message = success_equip_message
    event_mock.message.buttons = []

    result = is_character_equip_gun_select(event_mock)

    assert result is False


def test_is_character_equip_gun_select_happy_path():
    button_rod = AsyncMock()
    button_rod.text = '🔪 Удочка ученика [I]  (7/20)'
    button_return = AsyncMock()
    button_return.text = 'Назад'
    event_mock = Mock()
    event_mock.message.message = success_equip_message
    event_mock.message.buttons = [[button_rod, button_return]]

    result = is_character_equip_gun_select(event_mock)

    assert result is True
