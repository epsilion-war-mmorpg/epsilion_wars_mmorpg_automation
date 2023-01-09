from unittest.mock import Mock

from app.actions import search_enemy


async def test_search_enemy_happy_path(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456

    await search_enemy(event_mock)

    assert mocked_client_message_send.call_count == 1
