from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.captcha.resolvers import try_resolve


@pytest.mark.parametrize('payload, expected', [
    ('unknown question', False),
    ('На пути ты встретил капчу.\n столицa Эпсилионa - Нaпишите ответ с большой буквы.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', True),
    ('На пути ты встретил капчу.\n 2 делить нa 2 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', True),
])
def test_try_resolve_happy_path(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    answer = try_resolve(event_mock)

    assert answer.question == payload
    assert bool(answer.resolver_type) is expected
    assert bool(answer.answer) is expected
