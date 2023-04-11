"""Stats collector module."""
import logging
import time
from collections import Counter

from epsilion_wars_mmorpg_automation.notifications import send_desktop_notify


class StatsCollector:
    """Stats collector."""

    def __init__(self) -> None:
        """Set up empty collector."""
        self._counters_collector: Counter = Counter()
        self._start_time: float = time.time()

    def reset(self) -> None:
        """Reset stats."""
        self._counters_collector.clear()

    def inc_value(self, name: str, increment: int = 1) -> None:
        """Increment stats counter."""
        self._counters_collector[name] += increment

    def get_counters(self) -> list[tuple[str, int]]:
        """Get raw stats."""
        return self._counters_collector.most_common()

    def get_averages_per_hour(self) -> list[tuple[str, float]]:
        """Get average stats."""
        hours = self._collecting_time() / 60 / 60
        return [
            (name, counter / hours)
            for name, counter in self._counters_collector.items()
        ]

    def _collecting_time(self) -> float:
        return time.time() - self._start_time


collector = StatsCollector()


async def show_stats() -> None:
    """Send stats to logs and notify."""
    logging.info('Stats total: {0}'.format(collector.get_counters()))
    logging.info('Stats averages: {0}'.format(collector.get_averages_per_hour()))

    await _send_stats_notify()


async def _send_stats_notify() -> None:
    counters: list[str] = [
        f'{name}: {counter_value}'
        for name, counter_value in collector.get_counters()
    ]
    averages: list[str] = [
        '%s per hour: %.2f' % (name, counter_value)
        for name, counter_value in collector.get_averages_per_hour()
    ]

    message = 'Stats\n{0}\n{1}'.format(
        '\n'.join(counters),
        '\n'.join(averages),
    )

    await send_desktop_notify(message)
