"""Farming tool (grinding with auto-repair)."""
import logging
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import shared_state, stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, loop
from epsilion_wars_mmorpg_automation.trainer.handlers import common, farming, grinding


async def main(repair_locations_path: str = '') -> None:
    """Farming runner."""
    local_settings = {
        'minimum_hp_level_for_grinding': app_settings.minimum_hp_level_for_grinding,
        'auto_healing_enabled': app_settings.auto_healing_enabled,
        'select_combo_strategy': app_settings.select_combo_strategy,
        'stop_if_captcha_fire': app_settings.stop_if_captcha_fire,
        'notifications_enabled': app_settings.notifications_enabled,
        'slow_mode': app_settings.slow_mode,
        'repair_locations_path': app_settings.repair_locations_path,
    }
    repair_locations_path = repair_locations_path or app_settings.repair_locations_path
    logging.info(f'start farming ({local_settings=}), {repair_locations_path}')

    shared_state.REPAIR_LOCATIONS_PATH = repair_locations_path.split(',')

    logging.info('auth as %s', (await client.get_me()).username)

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

    await action.common_actions.ping(game_user.user_id)
    await loop.run_wait_loop(None)
    logging.info('end farming')


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    if isinstance(event, events.MessageEdited.Event):
        # update handlers for repairing here
        select_callback = _select_action_by_event_update(event)

    else:
        select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.common_states.is_captcha_message, common.captcha_fire_handler),
        (state.common_states.is_hp_updated_message, action.common_actions.ping),
        (state.common_states.is_equip_broken_message, farming.equip_broken_handler),
        (state.grinding_states.is_battle_start_message, grinding.battle_start_handler),
        (state.grinding_states.is_selector_combo, action.grinding_actions.select_combo),
        (state.grinding_states.is_selector_attack_direction, action.grinding_actions.select_attack_direction),
        (state.grinding_states.is_selector_defence_direction, action.grinding_actions.select_defence_direction),
        (state.grinding_states.is_win_state, grinding.battle_end_handler),
        (state.grinding_states.is_died_state, farming.battle_end_handler),

        (state.reward_states.is_reward_catch_message, action.common_actions.ping),
        (state.reward_states.is_reward_already_used_message, action.common_actions.ping),
        (state.reward_states.is_daily_reward_found, action.reward_actions.catch_reward),
        (state.reward_states.is_daily_reward_not_found, action.common_actions.ping),
        (state.reward_states.is_reward_recipient_selector, action.reward_actions.select_reward_recipient),

        (state.grinding_states.is_grinding_ready_state, farming.farming_handler),
        (state.common_states.is_map_open_state, farming.go_to_handler),
        (state.common_states.is_town, farming.repair_or_go_to_next),

        (state.common_states.is_npc_selector, farming.repairman_call),
        (state.farming_states.is_repair_button_available, farming.repair_start),
        (state.vendor_states.is_random_vendor_meet, farming.skip_vendor),
        (state.vendor_states.is_random_vendor_meet_exit, action.common_actions.exit_after_vendor),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler


def _select_action_by_event_update(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.farming_states.is_repair_item_selector, farming.repair_item),
        (state.farming_states.is_repair_item_approve_request, farming.repair_item_approve),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler
