import pytest

from epsilion_wars_mmorpg_automation.captcha.game_specific import game_specific


@pytest.mark.parametrize('payload, expected_answer', [
    ('неподдерживаемый пример', None),

    ('На пути ты встретил капчу.\n столицa Эпсилионa - Нaпишите ответ с большой буквы.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', 'Мелидон'),
    ('На пути ты встретил капчу.\n столицa Эпсилионa - Нaпишите ответ с маленькой буквы.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', 'мелидон'),
])
def test_game_specific_happy_path(payload: str, expected_answer: str | None):
    result = game_specific(payload)

    assert result == expected_answer
