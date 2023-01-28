from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.actions import select_attack_direction
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError


async def test_select_attack_direction_happy_path(mocked_client_message_send):
    button_first = Mock()
    button_first.text = 'first'
    button_second = Mock()
    button_second.text = 'second'
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = [[button_first, button_second]]

    await select_attack_direction(event_mock)

    assert mocked_client_message_send.call_count == 1


@pytest.mark.parametrize('buttons', [
    None,
    [],
])
async def test_select_attack_direction_buttons_not_found(mocked_client_message_send, buttons):
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = buttons

    with pytest.raises(InvalidMessageError):
        await select_attack_direction(event_mock)
