"""Command-line interface."""
import argparse
import logging
import signal
from typing import Any, Callable

from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import captcha_solver, daily_reward_catcher, fishing, grinding, inventory, loop


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
    _run(grinding.main, args.minutes_limit)


def captcha_solver_start() -> None:
    """Start captcha-solver."""
    _run(captcha_solver.main)


def daily_reward_catcher_start() -> None:
    """Start daily reward catcher."""
    _run(daily_reward_catcher.main)


def fishing_start() -> None:
    """Start fishing."""
    _run(fishing.main)


def inventory_start() -> None:
    """Start one time inventory."""
    parser = argparse.ArgumentParser(description='Start inventory.')
    parser.add_argument(
        '-t',
        '--type',
        required=False,
        default='receipt',
        choices=['resource', 'receipt', 'scroll', 'potion', 'other'],
        help='Select resources type',
    )
    args = parser.parse_args()
    _run(inventory.main, selected_type=args.type)


def _run(main_func: Callable, *args: Any, **kwargs: Any) -> None:
    _setup_logging()
    signal.signal(signal.SIGINT, loop.exit_request)
    try:
        with client:
            client.loop.run_until_complete(main_func(*args, **kwargs))
    except ConnectionError:
        loop.exit_request()


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
