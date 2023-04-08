"""Lock utils."""

import time

from epsilion_wars_mmorpg_automation.settings import app_settings

_timers: dict[str, int] = {}


def healing_available() -> bool:
    """Return True if healing available for execute by throttling timer."""
    key = 'healing'
    current_time = int(time.time())
    time_after_last_execution = current_time - _timers.get(key, 0)
    if time_after_last_execution >= app_settings.healing_timeout:
        _timers[key] = current_time
        return True
    return False
