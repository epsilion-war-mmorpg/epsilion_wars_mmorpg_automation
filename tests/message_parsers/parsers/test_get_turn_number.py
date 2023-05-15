import pytest

from epsilion_wars_mmorpg_automation.game.parsers import get_turn_number

valid_turn_start_template = """Ход {0}

🐺 🤴jdjdjhf 🔸31 ❤️(1234/2345) бьет в голову.  🥊 И критом пробивает блок противника на 💥 233 урона


🕸🧟‍♂️ Древний зомби 🔸31 ❤️️(234/123) бьет в грудь и наносит 111



🗡0🛡0🥊1⚡0🤺0🌬1"""


@pytest.mark.parametrize('payload, expected', [
    (valid_turn_start_template.format(1), 1),
    (valid_turn_start_template.format(666), 666),
    ('Куда будешь бить?', 0),
])
def test_get_turn_number(payload: str, expected: int):
    result = get_turn_number(payload)

    assert result == expected
