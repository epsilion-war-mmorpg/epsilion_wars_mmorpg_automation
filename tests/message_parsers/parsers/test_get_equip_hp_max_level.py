import pytest

from epsilion_wars_mmorpg_automation.game.parsers import get_equip_hp_max_level


@pytest.mark.parametrize('payload,expected', [
    ('ледяной марион провидца [iii+] +6 (17/1)', 1),
    ('🔪 Удочка подмастерья [II]  (30/30)', 30),
    ('🧟‍♂Ник ащет 🔸9 ❤️(', 0),
])
def test_get_equip_hp_level_happy_path(payload: str, expected: int):
    result = get_equip_hp_max_level(payload)

    assert result == expected
