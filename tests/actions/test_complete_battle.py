from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.actions import complete_battle


async def test_complete_battle_happy_path(mocked_client_message_send):
    button_mock = Mock()
    button_mock.text = 'Win or defeat'
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.buttons = [[button_mock]]

    await complete_battle(event_mock)

    assert mocked_client_message_send.call_count == 1
