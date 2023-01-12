"""Seek mobs and kill them."""
import asyncio
import logging
import time
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import actions
from epsilion_wars_mmorpg_automation.message_parsers import checks, parsers
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client

_has_stop_request: bool = False


async def main(execution_limit_minutes: int | None = None) -> None:
    """Grinding runner."""
    local_settings = {
        'execution_limit_minutes': execution_limit_minutes or 'infinite',
        'minimum_hp_level_for_grinding': app_settings.minimum_hp_level_for_grinding,
        'auto_healing_enabled': app_settings.auto_healing_enabled,
    }
    logging.info(f'start grinding ({local_settings=})')
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

    await actions.ping(game_user.user_id)

    await _run_wait_loop(execution_limit_minutes)
    logging.info('end grinding by time left')


def sigint_handler(current_signal, frame) -> None:  # type: ignore
    global _has_stop_request
    _has_stop_request = True


async def _run_wait_loop(execution_limit_minutes: int | None) -> None:
    start_time = time.time()
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
        execution_time = time.time() - start_time


async def _grind_handler(event: events.NewMessage.Event) -> None:
    message_content = parsers.strip_message(event.message.message)
    logging.info('handle event %s', message_content[:app_settings.message_log_limit])

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (checks.is_selector_combo, actions.select_combo),
        (checks.is_selector_attack_direction, actions.select_attack_direction),
        (checks.is_selector_defence_direction, actions.select_defence_direction),
        (checks.is_win_state, actions.complete_battle),
        (checks.is_died_state, actions.complete_battle),
        (checks.is_hp_updated_message, actions.ping),
        (checks.is_hunting_ready_message, _hunting_optional),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return _skip_event


async def _hunting_optional(event: events.NewMessage.Event) -> None:
    hp_level_percent = parsers.get_hp_level(
        message_content=parsers.strip_message(event.message.message),
    )
    logging.info('current HP level is %d%%', hp_level_percent)

    if hp_level_percent >= app_settings.minimum_hp_level_for_grinding:
        await actions.search_enemy(event)

    elif app_settings.auto_healing_enabled:
        await actions.healing(event)


async def _skip_event(event: events.NewMessage.Event) -> None:
    logging.debug('skip event')
