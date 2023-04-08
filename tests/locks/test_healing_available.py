import asyncio

from epsilion_wars_mmorpg_automation import locks
from epsilion_wars_mmorpg_automation.settings import app_settings


def test_healing_available_lock_free():
    result = locks.healing_available()

    assert result is True


def test_healing_available_locked():
    locks.healing_available()

    result = locks.healing_available()

    assert result is False


async def test_healing_available_lock_released():
    locks.healing_available()
    await asyncio.sleep(app_settings.healing_timeout)

    result = locks.healing_available()

    assert result is True

