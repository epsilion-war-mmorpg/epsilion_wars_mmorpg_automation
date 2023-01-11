import pytest

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.message_parsers.parsers import get_character_level


@pytest.mark.parametrize('payload,expected', [
    ('🧟‍♂Dfd 🔸1 ❤️(463/506)\n🔸 Уровень монстров: 7-10', 1),
    ('🧟‍♂Unikcname 🔸10 ❤️(509/509)\n🔸 Уровень монстров: 7-10', 10),
    ('🧟‍♂Ник ащет 🔸39 ❤️(1/509)\n🔸 Уровень монстров: 7-10', 39),
])
def test_get_character_level_happy_path(payload: str, expected: int):
    result = get_character_level(payload)

    assert result == expected


def test_get_character_level_not_found():
    with pytest.raises(InvalidMessageError):
        get_character_level('')
