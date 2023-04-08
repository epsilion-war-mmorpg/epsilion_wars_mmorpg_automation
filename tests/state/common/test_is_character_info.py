from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.common import is_character_info

success_equip_message = """🐺 🤴Дикость 🔸29 ❤️(12345/23456)

💰 Золото: 232323
🍪 Печеньки: 232

🔸 Уровень: 13
✨ Опыт: 3435/1000000
🏵 Слава: 345 (Барон)

🔋 Очков энергии: (1/15)


🧬 Очков параметров: 0

➕ Бонус к опыту: 1%
➕ Бонус к золоту: 0%
➕ Бонус к дропу: 6%"""


def test_is_character_info():
    event_mock = Mock()
    event_mock.message.message = success_equip_message

    result = is_character_info(event_mock)

    assert result is True

