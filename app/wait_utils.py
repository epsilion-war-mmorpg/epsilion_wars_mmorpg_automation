"""Random freezes like real-human."""

import asyncio
import logging
import random


async def wait_for(min_seconds: int, max_seconds: int) -> None:
    """Lets wait like human =)."""
    sleep_time = random.randint(min_seconds, max_seconds)
    logging.debug('wait like human %d seconds before action', sleep_time)
    await asyncio.sleep(sleep_time)
