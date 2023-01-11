from epsilion_wars_mmorpg_automation.actions import ping


async def test_ping_happy_path(mocked_client_message_send):
    await ping(123456)

    assert mocked_client_message_send.call_count == 1
