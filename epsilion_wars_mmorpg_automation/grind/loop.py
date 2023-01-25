"""Main execution loop for grinding process."""

import asyncio
import logging
import time

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.settings import app_settings

_has_stop_request: bool = False


def exit_request(*args, **kwargs) -> None:  # type: ignore
    """Stop training signal by request."""
    global _has_stop_request  # noqa: WPS420, WPS442
    _has_stop_request = True  # noqa: WPS122, WPS442
    logging.info('force exit')


async def run_wait_loop(execution_limit_minutes: int | None) -> None:
    """Wait execution time left or stop signals."""
    start_time = time.time()
    stats_show_time = start_time
    execution_time = float(0)
    time_limit = (execution_limit_minutes or 0) * 60

    while True:
        if time_limit and execution_time >= time_limit:
            logging.info('stop training by time left')
            break

        if _has_stop_request:
            logging.info('stop training by request')
            break

        logging.debug('next wait iteration')
        await asyncio.sleep(app_settings.wait_loop_iteration_seconds)
        current_time = time.time()
        execution_time = current_time - start_time

        if int(current_time - stats_show_time) >= app_settings.show_stats_every_seconds:
            stats_show_time = current_time
            await stats.show_stats()

    await stats.show_stats()
