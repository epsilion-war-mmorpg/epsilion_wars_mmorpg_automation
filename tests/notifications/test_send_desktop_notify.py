import pytest

from epsilion_wars_mmorpg_automation.notifications import send_desktop_notify


@pytest.mark.parametrize('payload', [
    'text\nmessage\nmultiline',
    'text message',
])
async def test_send_desktop_notify_happy_path(payload: str):
    await send_desktop_notify(payload)

    assert True
