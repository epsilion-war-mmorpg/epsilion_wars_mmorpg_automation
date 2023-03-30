import pytest

from epsilion_wars_mmorpg_automation.game.state.fishing import is_rod_equip_needed


@pytest.mark.parametrize('payload, expected', [
    ('Нужно надеть удочку!', True),
    ('Недостаточно прочности у удочки!', True),
    ('рандомное сообщение', False),
])
def test_is_rod_equip_needed_happy_path(payload: str, expected: bool):
    result = is_rod_equip_needed(payload)

    assert result is expected
