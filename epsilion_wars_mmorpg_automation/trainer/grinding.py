"""Grinding tool."""
import logging
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game.action import common as common_actions
from epsilion_wars_mmorpg_automation.game.action import grinding as grinding_actions
from epsilion_wars_mmorpg_automation.game.state import common as common_states
from epsilion_wars_mmorpg_automation.game.state import grinding as grinding_states
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, loop
from epsilion_wars_mmorpg_automation.trainer.handlers import common, grinding


async def main(execution_limit_minutes: int | None = None) -> None:
    """Grinding runner."""
    local_settings = {
        'execution_limit_minutes': execution_limit_minutes or 'infinite',
        'minimum_hp_level_for_grinding': app_settings.minimum_hp_level_for_grinding,
        'auto_healing_enabled': app_settings.auto_healing_enabled,
        'select_combo_strategy': app_settings.select_combo_strategy,
        'stop_if_equip_broken': app_settings.stop_if_equip_broken,
        'stop_if_captcha_fire': app_settings.stop_if_captcha_fire,
        'notifications_enabled': app_settings.notifications_enabled,
        'slow_mode': app_settings.slow_mode,
    }
    logging.info('start grinding ({0})'.format(local_settings))
    logging.info('move u character to hunting location first')

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

    await common_actions.ping(game_user.user_id)

    await loop.run_wait_loop(execution_limit_minutes)
    logging.info('end grinding')


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (common_states.is_captcha_message, common.captcha_fire_handler),
        (common_states.is_equip_broken_message, grinding.equip_broken_handler),
        (grinding_states.is_battle_start_message, grinding.battle_start_handler),
        (grinding_states.is_selector_combo, grinding_actions.select_combo),
        (grinding_states.is_selector_attack_direction, grinding_actions.select_attack_direction),
        (grinding_states.is_selector_defence_direction, grinding_actions.select_defence_direction),
        (grinding_states.is_win_state, grinding.battle_end_handler),
        (grinding_states.is_died_state, grinding.battle_end_handler),
        (common_states.is_hp_updated_message, common_actions.ping),
        (grinding_states.is_grinding_ready_state, grinding.grinding_handler),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler
