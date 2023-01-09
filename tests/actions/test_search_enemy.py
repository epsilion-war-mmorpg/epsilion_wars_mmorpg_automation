from unittest.mock import Mock

from app.actions import search_enemy


async def test_search_enemy_happy_path(mocker):
    client_mock = mocker.patch('app.actions.client.send_message')
    event_mock = Mock()
    event_mock.chat_id = 123456

    await search_enemy(event_mock)

    assert client_mock.call_count == 1
