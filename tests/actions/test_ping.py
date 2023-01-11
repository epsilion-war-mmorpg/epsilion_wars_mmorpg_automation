from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.actions import ping


async def test_ping_happy_path(mocked_client_message_send):
    await ping(123456)

    assert mocked_client_message_send.call_count == 1


async def test_ping_by_event_entity(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456

    await ping(event_mock)

    assert mocked_client_message_send.call_count == 1
