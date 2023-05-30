from unittest.mock import AsyncMock

import pytest

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.action.rewards import select_reward_recipient


async def test_select_reward_recipient_happy_path():
    button_first = AsyncMock()
    button_first.text = '🧝\u200d♂️️ Дичина 🔸5'
    button_second = AsyncMock()
    button_second.text = '🤴️ Бесогончик 🔸32 🔘'
    button_last = AsyncMock()
    button_last.text = '🧟\u200d♂️ Ololo 🔸31'
    event_mock = AsyncMock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = [[button_first, button_second], [button_last]]

    await select_reward_recipient(event_mock)

    assert event_mock.message.click.call_count == 1


@pytest.mark.parametrize('buttons', [
    None,
    [],
])
async def test_select_reward_recipient_buttons_not_found(mocked_client_message_send, buttons):
    event_mock = AsyncMock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = buttons

    with pytest.raises(InvalidMessageError):
        await select_reward_recipient(event_mock)
