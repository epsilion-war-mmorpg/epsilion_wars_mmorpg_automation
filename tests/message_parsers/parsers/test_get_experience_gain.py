import pytest

from epsilion_wars_mmorpg_automation.game.parsers import get_experience_gain


@pytest.mark.parametrize('payload, expected', [
    ('📍 Ты победил своего врага -  💀 Скелет в доспехах 🔸14 💔\n\nПолучено в награду:\n✨ Опыта: 64\n💰 Золота: 6', 64),
    ('Тебя убил: ☠️ Гигантский скелет 🔸14\n\nТы был отправлен восстанавливаться в город', 0),
])
def test_get_experience_gain(payload: str, expected: int):
    result = get_experience_gain(payload)

    assert result == expected
