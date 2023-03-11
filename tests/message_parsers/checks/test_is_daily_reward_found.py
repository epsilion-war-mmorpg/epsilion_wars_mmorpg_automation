from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.rewards import is_daily_reward_found


@pytest.mark.parametrize('button_text,expected', [
    ('🧁  Ежедневная награда (❗️1)', True),
    ('🧁  Ежедневная награда (❗️2)', True),
    ('🧁  Ежедневная награда', False),
    ('Непонятная кнопка', False),
])
def test_is_daily_reward_found(button_text: str, expected: bool):
    button = Mock()
    button.text = button_text
    event_mock = Mock()
    event_mock.message.message = ''
    event_mock.message.button_count = 1
    event_mock.message.buttons = [[button]]

    result = is_daily_reward_found(event_mock)

    assert result is expected
