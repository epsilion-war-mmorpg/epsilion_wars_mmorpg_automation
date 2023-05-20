"""Hunting tool."""
import asyncio
import logging
import random
import time
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, loop
from epsilion_wars_mmorpg_automation.trainer.handlers import common, hunting


async def main() -> None:
    """Hunting runner."""
    logging.info('start hunting')

    game_user: types.InputPeerUser = await client.get_input_entity(game_bot_name)
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
    await _try_hunting_periodically(game_user)

    logging.info('end hunting')


async def _try_hunting_periodically(game_user: types.InputPeerUser) -> None:
    start_time = time.time()
    next_try_timer = random.randint(
        app_settings.check_hunting_every_seconds_min,
        app_settings.check_hunting_every_seconds_max,
    )
    logging.info(f'next try timer {next_try_timer}')

    # check immediately after run
    await action.hunting_actions.start_hunt(game_user.user_id)

    while True:
        if loop.has_exit_request():
            logging.info('stop by request')
            break

        timer = time.time() - start_time
        if timer >= next_try_timer:
            start_time = time.time()
            next_try_timer = random.randint(
                app_settings.check_hunting_every_seconds_min,
                app_settings.check_hunting_every_seconds_max,
            )
            await action.hunting_actions.start_hunt(game_user.user_id)
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
        (state.hunting_states.is_hunting_type_selector, hunting.hunting_start),
        (state.common_states.is_character_equip_select, action.common_actions.show_equip_guns),
        (state.hunting_states.is_hunting_end, hunting.hunting_end),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.info('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler


def _select_action_by_event_update(event: events.MessageEdited.Event) -> Callable:
    mapping = [
        (state.common_states.is_character_equip_gun_select, action.hunting_actions.equip_bow),
        (state.hunting_states.is_equip_bow_state, action.hunting_actions.equip_use),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.info('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler
