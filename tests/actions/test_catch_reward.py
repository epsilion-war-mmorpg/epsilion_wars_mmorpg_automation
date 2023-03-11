from unittest.mock import AsyncMock

import pytest

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.action.rewards import catch_reward


async def test_catch_reward_happy_path(mocked_client_message_send):
    button_first = AsyncMock()
    button_first.text = 'first'
    button_second = AsyncMock()
    button_second.text = 'second'
    event_mock = AsyncMock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = [[button_first, button_second]]

    await catch_reward(event_mock)

    assert mocked_client_message_send.call_count == 1


@pytest.mark.parametrize('buttons', [
    None,
    [],
])
async def test_catch_reward_buttons_not_found(mocked_client_message_send, buttons):
    event_mock = AsyncMock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = buttons

    with pytest.raises(InvalidMessageError):
        await catch_reward(event_mock)

    assert mocked_client_message_send.call_count == 0

