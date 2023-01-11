from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.actions import complete_battle


async def test_complete_battle_happy_path(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456

    await complete_battle(event_mock)

    assert mocked_client_message_send.call_count == 1
