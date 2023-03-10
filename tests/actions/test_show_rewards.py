from epsilion_wars_mmorpg_automation.game.actions import show_rewards


async def test_show_rewards_happy_path(mocked_client_message_send):
    await show_rewards(123456)

    assert mocked_client_message_send.call_count == 1
