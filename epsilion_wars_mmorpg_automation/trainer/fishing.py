"""Fishing tool."""
import asyncio
import logging
import random
import time
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, handlers, loop


async def main() -> None:
    """Fishing runner."""
    logging.info('start fishing')

    game_user: types.InputPeerUser = await client.get_input_entity(app_settings.game_username)
    logging.info('game user is %s', game_user)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )
    client.add_event_handler(
        callback=_message_handler,
        event=events.MessageEdited(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    # run checker time to time
    await _try_fishing_periodically(game_user)

    logging.info('end fishing')


async def _try_fishing_periodically(game_user: types.InputPeerUser) -> None:
    start_time = time.time()
    next_try_timer = random.randint(
        app_settings.check_fishing_every_seconds_min,
        app_settings.check_fishing_every_seconds_max,
    )
    logging.info(f'next try timer {next_try_timer}')

    # check immediately after run
    await action.fishing_actions.start_fishing(game_user.user_id)

    while True:
        if loop.has_exit_request():
            logging.info('stop by request')
            break

        timer = time.time() - start_time
        if timer >= next_try_timer:
            start_time = time.time()
            next_try_timer = random.randint(
                app_settings.check_fishing_every_seconds_min,
                app_settings.check_fishing_every_seconds_max,
            )
            await action.fishing_actions.start_fishing(game_user.user_id)
            logging.info(f'next try timer {next_try_timer} {timer}')

        else:
            logging.debug('next wait iteration')
            await asyncio.sleep(app_settings.wait_loop_iteration_seconds)


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    if isinstance(event, events.MessageEdited.Event):
        select_callback = _select_action_by_event_update(event)
    else:
        select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.fishing_states.is_fishing_type_selector, handlers.fishing_start),
        (state.common_states.is_character_equip_select, action.common_actions.show_equip_guns),
        (state.fishing_states.is_fishing_end, action.fishing_actions.complete_fishing),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.info('is %s event', check_function.__name__)
            return callback_function

    return handlers.skip_turn_handler


def _select_action_by_event_update(event: events.MessageEdited.Event) -> Callable:
    mapping = [
        (state.common_states.is_character_equip_gun_select, action.fishing_actions.equip_rod),
        (state.fishing_states.is_equip_rod_state, action.common_actions.equip_use),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.info('is %s event', check_function.__name__)
            return callback_function

    return handlers.skip_turn_handler
