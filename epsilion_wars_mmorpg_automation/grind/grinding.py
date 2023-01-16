"""Grinding functionality and runner."""
import logging
import signal
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import actions
from epsilion_wars_mmorpg_automation.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.grind import handlers, loop
from epsilion_wars_mmorpg_automation.parsers import parsers
from epsilion_wars_mmorpg_automation.parsers.checks import messages, states
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client


async def main(execution_limit_minutes: int | None = None) -> None:
    """Grinding runner."""
    local_settings = {
        'execution_limit_minutes': execution_limit_minutes or 'infinite',
        'minimum_hp_level_for_grinding': app_settings.minimum_hp_level_for_grinding,
        'auto_healing_enabled': app_settings.auto_healing_enabled,
        'stop_if_equip_broken': app_settings.stop_if_equip_broken,
        'stop_if_captcha_fire': app_settings.stop_if_captcha_fire,
        'notifications_enabled': app_settings.notifications_enabled,
    }
    logging.info(f'start grinding ({local_settings=})')
    logging.info('move u character to hunting location first')

    me = await client.get_me()
    logging.info('auth as %s', me.username)

    game_user: types.InputPeerUser = await client.get_input_entity(app_settings.game_username)
    logging.debug('game user is %s', game_user)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    await actions.ping(game_user.user_id)

    await loop.run_wait_loop(execution_limit_minutes)
    logging.info('end grinding')


def setup_signals_handlers() -> None:
    """Set up signal handlers."""
    signal.signal(signal.SIGINT, loop.exit_request)


async def _message_handler(event: events.NewMessage.Event) -> None:
    _log_event_information(event)

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)

    await select_callback(event)


def _log_event_information(event: events.NewMessage.Event) -> None:
    message_content = parsers.strip_message(event.message.message)
    logging.info(
        'handle event message="%s"; buttons="%s"',
        message_content[:app_settings.message_log_limit],
        [button.text for button in get_buttons_flat(event)],
    )


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (messages.is_captcha_message, handlers.captcha_fire_handler),
        (messages.is_equip_broken_message, handlers.equip_broken_handler),
        (messages.is_battle_start_message, handlers.battle_start_handler),
        (states.is_selector_combo, actions.select_combo),
        (states.is_selector_attack_direction, actions.select_attack_direction),
        (states.is_selector_defence_direction, actions.select_defence_direction),
        (states.is_win_state, handlers.battle_end_handler),
        (states.is_died_state, handlers.battle_end_handler),
        (messages.is_hp_updated_message, actions.ping),
        (messages.is_hunting_ready_message, handlers.hunting_handler),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return handlers.skip_turn_handler
