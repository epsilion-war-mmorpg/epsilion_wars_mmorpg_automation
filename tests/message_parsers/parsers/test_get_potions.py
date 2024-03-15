import pytest

from epsilion_wars_mmorpg_automation.game.parsers import get_potions

potions_message = """🧪 Зелья

💚 Личный бонус регенерации 24ч - 1шт /use_reg24
🔋 Личный Энергетик - 3шт /use_p_energy
Можно использовать не более 12 раз за день.
🧪 Эликсир здоровья +25% [II] - 2шт /use_low_hpII"""


@pytest.mark.parametrize('payload, expected', [
    (potions_message, ['/use_reg24', '/use_p_energy', '/use_low_hpII']),
    ('🧪 Зелья\n\n❓ Зелий готовых для использования - нет', []),
])
def test_get_potions(payload: str, expected: int):
    result = get_potions(payload)

    assert result == expected
