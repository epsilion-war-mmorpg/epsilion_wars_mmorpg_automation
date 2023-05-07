"""Daily reward catcher tool."""
import asyncio
import logging
import time
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, loop
from epsilion_wars_mmorpg_automation.trainer.handlers import common


async def main() -> None:
    """Reward-catcher runner."""
    logging.info('start reward-catcher')

    game_user: types.InputPeerUser = await client.get_input_entity(game_bot_name)
    logging.info('game user is %s', game_user)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    # run checker time to time
    await _check_reward_periodically(game_user)

    logging.info('end reward-catcher')


async def _check_reward_periodically(game_user: types.InputPeerUser) -> None:
    start_time = time.time()

    # check immediately after run
    await action.reward_actions.show_rewards(game_user.user_id)

    while True:
        if loop.has_exit_request():
            logging.info('stop by request')
            break

        timer = time.time() - start_time
        if timer >= app_settings.check_rewards_every_seconds:
            start_time = time.time()
            await action.reward_actions.show_rewards(game_user.user_id)

        else:
            logging.debug('next wait iteration')
            await asyncio.sleep(app_settings.wait_loop_iteration_seconds)


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    select_callback = _select_action_by_event(event)

    await select_callback(event)


def _select_action_by_event(event: events.NewMessage.Event) -> Callable:
    mapping = [
        (state.reward_states.is_reward_catch_message, action.common_actions.ping),
        (state.reward_states.is_reward_already_used_message, action.common_actions.ping),
        (state.reward_states.is_daily_reward_found, action.reward_actions.catch_reward),
        (state.reward_states.is_daily_reward_not_found, action.common_actions.ping),
        (state.reward_states.is_reward_recipient_selector, action.reward_actions.select_reward_recipient),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler
