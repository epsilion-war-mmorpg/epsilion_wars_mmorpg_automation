"""Seek mobs and kill them."""
import asyncio
import logging
import time
from typing import Callable

from telethon import events, types

from app.actions import complete_battle, ping, search_enemy, select_attack_direction, select_defence_direction
from app.message_parsers import checks, parsers
from app.settings import app_settings
from app.telegram_client import client


async def main(execution_limit_minutes: int | None = None) -> None:
    """Grinding runner."""
    logging.info('start grinding (%d)', execution_limit_minutes)
    logging.info('move u character to hunting location first')

    me = await client.get_me()
    logging.info('auth as %s', me.username)

    game_user: types.InputPeerUser = await client.get_input_entity(app_settings.game_username)
    logging.debug('game user is %s', game_user)

    client.add_event_handler(
        callback=_grind_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    await ping(game_user.user_id)

    await _run_wait_loop(execution_limit_minutes)
    logging.info('end grinding by time left')


async def _run_wait_loop(execution_limit_minutes: int | None) -> None:
    start_time = time.time()
    execution_time = float(0)
    time_limit = (execution_limit_minutes or 0) * 60

    while not time_limit or execution_time < time_limit:
        await asyncio.sleep(10)
        logging.debug('next iteration')
        execution_time = time.time() - start_time


async def _grind_handler(event: events.NewMessage.Event) -> None:
    message_content = parsers.strip_message(event.message.message)
    logging.info('handle event %s', message_content[:app_settings.message_log_limit])

    select_callback = _select_action_by_event(event)
    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (checks.is_selector_attack_direction, select_attack_direction),
        (checks.is_selector_defence_direction, select_defence_direction),
        (checks.is_hp_full_message, search_enemy),
        (checks.is_win_state, complete_battle),
        (checks.is_died_state, _end_game),
        (checks.is_hunting_ready_message, _hunting_optional),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return _skip_event


async def _end_game(event: events.NewMessage.Event) -> None:
    raise RuntimeError('U died :RIP:')


async def _hunting_optional(event: events.NewMessage.Event) -> None:
    hp_level_percent = parsers.get_hp_level(
        message_content=parsers.strip_message(event.message.message),
    )
    logging.info('current HP level is %d%%', hp_level_percent)
    if hp_level_percent >= app_settings.minimum_hp_level_for_grinding:
        await search_enemy(event)


async def _skip_event(event: events.NewMessage.Event) -> None:
    logging.debug('skip event')


if __name__ == '__main__':
    # todo getopt timelimit
    # todo getopt debug
    max_time = 25

    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    with client:
        client.loop.run_until_complete(main(max_time))
