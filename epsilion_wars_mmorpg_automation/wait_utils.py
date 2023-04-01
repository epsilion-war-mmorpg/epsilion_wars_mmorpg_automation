"""Random freezes like real-human."""

import asyncio
import enum
import logging
import random

from epsilion_wars_mmorpg_automation.settings import app_settings


class WaitActions(enum.Enum):
    """
    Timings for game actions.

    Format: NAME = (min, max, min_slow_mode, max_slow_mode)
    """

    COMMON = (1, 3, 9, 19)
    CAPTCHA = (4, 9, 5, 10)
    HUNTING_START = (3, 8, 5, 10)


async def wait_for(timing: WaitActions = WaitActions.COMMON) -> None:
    """Lets wait like human =)."""
    min_seconds, max_seconds, min_slow_mode, max_slow_mode = timing.value
    if app_settings.slow_mode:
        sleep_time = random.randint(min_slow_mode, max_slow_mode)
    else:
        sleep_time = random.randint(min_seconds, max_seconds)
    logging.debug('wait like human %d seconds before action', sleep_time)
    await asyncio.sleep(sleep_time)
