"""Command-line interface."""
import argparse
import logging

from epsilion_wars_mmorpg_automation.grind import grinding
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client


def grind_start() -> None:
    """Start grinding."""
    parser = argparse.ArgumentParser(description='Start grinding.')
    parser.add_argument(
        '-t',
        '--minutes',
        dest='minutes_limit',
        required=False,
        type=int,
        help='Execution limit in minutes',
    )
    args = parser.parse_args()

    _setup_logging()
    grinding.setup_signals_handlers()
    with client:
        client.loop.run_until_complete(grinding.main(args.minutes_limit))


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
