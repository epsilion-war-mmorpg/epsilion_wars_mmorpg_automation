from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.rewards import is_reward_already_used_message


@pytest.mark.parametrize('payload,expected', [
    (
        '🧁  Ежедневная награда\n\nТы уже получил награду сегодня',
        True,
    ),
    (
        '🧁  Ежедневная награда\n\nТвоя награда сегодня:\n🛑🔥 Обожженный философский камень 2шт\n\nКакому персонажу ее отправить?',
        False,
    ),
    (
        '🧁  Ежедневная награда\n\nДень 11\nТвоя награда - 🛑🔥 Обожженный философский камень 2шт',
        False,
    ),
    ('ololo', False),
])
def test_is_reward_already_used_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_reward_already_used_message(event_mock)

    assert result is expected
