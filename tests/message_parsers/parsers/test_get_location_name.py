import pytest

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.parsers import get_location_name


@pytest.mark.parametrize('payload,expected', [
    ('💧 Спуск к воде\n\nС виду о. Эпсил довольно спокойно. Однако, не стоит долго', '💧 Спуск к воде'),
    ('🏞🏛 Озеро Эпсил\n\nОзеро, названое в честь Эпсила, предыдущего правителя Эпсилиона.', '🏞🏛 Озеро Эпсил'),
    ('🗿🏛 Древние руины\n\nМного веков назад 🌋 Вулкан не пощадил древнюю цивилизацию, жившую в этом городе.', '🗿🏛 Древние руины'),
])
def test_get_location_name_happy_path(payload: str, expected: int):
    result = get_location_name(payload)

    assert result == expected


def test_get_location_level_not_found():
    with pytest.raises(InvalidMessageError):
        get_location_name('')
