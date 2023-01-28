from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.actions import healing


# async def test_healing_happy_path(mocked_client_message_send):
async def test_healing_skip_high_level_guys(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.message = '🧟‍♂Unikcname 🔸20 ❤️(25/100)'

    await healing(event_mock)

    assert mocked_client_message_send.call_count == 0

async def test_healing_skip_high_HP(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456
    event_mock.message.message = '🧟‍♂Unikcname 🔸20 ❤️(75/100)'

    await healing(event_mock)

    assert mocked_client_message_send.call_count == 0
