from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.action.hunting import select_combo
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError


async def test_select_combo_happy_path(mocked_client_message_send):
    button_first = Mock()
    button_first.text = 'Комбо удар!'
    button_second = Mock()
    button_second.text = 'Пропустить'
    button_last = Mock()
    button_last.text = 'Сбежать'
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = [[button_first, button_second, button_last]]

    await select_combo(event_mock)

    assert mocked_client_message_send.call_count == 1


@pytest.mark.parametrize('buttons', [
    None,
    [],
    [[1, 2]],
])
async def test_select_combo_buttons_not_found(mocked_client_message_send, buttons):
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = buttons

    with pytest.raises(InvalidMessageError):
        await select_combo(event_mock)
