"""Grinding tool."""
import logging
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, handlers, loop
from epsilion_wars_mmorpg_automation.trainer.handlers_ import farming


async def main() -> None:
    """Farming runner."""
    local_settings = {
        'minimum_hp_level_for_grinding': app_settings.minimum_hp_level_for_grinding,
        'auto_healing_enabled': app_settings.auto_healing_enabled,
        'stop_if_captcha_fire': app_settings.stop_if_captcha_fire,
        'notifications_enabled': app_settings.notifications_enabled,
        'slow_mode': app_settings.slow_mode,
    }
    logging.info(f'start farming ({local_settings=})')
    logging.info('move u character to farming location first')

    me = await client.get_me()
    logging.info('auth as %s', me.username)

    game_user: types.InputPeerUser = await client.get_input_entity(game_bot_name)
    logging.info('game user is %s', game_user)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    await action.common_actions.ping(game_user.user_id)

    await loop.run_wait_loop(None)
    logging.info('end farming')


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)
    # todo repair equip handlers here

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.common_states.is_captcha_message, handlers.captcha_fire_handler),
        (state.common_states.is_equip_broken_message, farming.equip_broken_handler),
        (state.grinding_states.is_battle_start_message, handlers.battle_start_handler),
        (state.grinding_states.is_selector_combo, action.grinding_actions.select_combo),
        (state.grinding_states.is_selector_attack_direction, action.grinding_actions.select_attack_direction),
        (state.grinding_states.is_selector_defence_direction, action.grinding_actions.select_defence_direction),
        (state.grinding_states.is_win_state, farming.battle_end_handler),
        (state.grinding_states.is_died_state, farming.battle_end_handler),
        (state.common_states.is_hp_updated_message, farming.hp_updated_handler),
        (state.common_states.is_map_open_state, farming.go_to_town_for_repair_handler),
        (state.grinding_states.is_hunting_ready_state, farming.farming_handler),

        # todo if current location is city - check current state and optionally try to repair
        # todo if state.to_grinding_zone: call "1" and go to grinding zone
        # todo if state.need_repair: set state.to_grinding_zone
        # todo if state.need_repair: call repair NPC
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return handlers.skip_turn_handler
