"""Inventory collector."""
import logging
from typing import Callable

from telethon import events, types

from epsilion_wars_mmorpg_automation import shared_state, stats
from epsilion_wars_mmorpg_automation.game import action, state
from epsilion_wars_mmorpg_automation.notifications import send_favorites_notify
from epsilion_wars_mmorpg_automation.settings import app_settings, game_bot_name
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, loop
from epsilion_wars_mmorpg_automation.trainer.handlers import common


async def main(selected_type: str) -> None:
    """Inventory collector runner."""
    logging.info(f'start inventory "{selected_type}"')
    shared_state.RESOURCE_TYPE = selected_type

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

    await _start(game_user.user_id)
    logging.info('end inventory')


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
        (state.inventory_states.is_resource_type_selector, action.inventory_actions.show_resource_type),
        (state.common_states.is_character_info, action.inventory_actions.save_character_name),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler


def _select_action_by_event_update(event: events.MessageEdited.Event) -> Callable:
    mapping = [
        (state.inventory_states.is_resource_pagination, common.collect_resource_counters),
    ]

    for check_function, callback_function in mapping:
        if check_function(event):
            logging.debug('is %s event', check_function.__name__)
            return callback_function

    return common.skip_turn_handler


async def _send_counters(counters: dict[str, int], character_name: str) -> None:
    if not counters:
        message = 'Ресурсы не найдены! =('
        logging.warning(message)
        return

    sorted_resources = sorted([
        '{0} - {1} шт.'.format(title, amount)
        for title, amount in counters.items()
    ])
    for index in range(0, len(sorted_resources), 60):
        message = '{0}:\n\n{1}\n\nПодготовлено с помощью [The Epsilion Trainer]({2}) (с)'.format(
            character_name,
            '\n'.join(sorted_resources[index:index + 60]),
            app_settings.trainer_public_link,
        )
        logging.info(message)
        await send_favorites_notify(message)


async def _start(game_user_id: int) -> None:
    # run show inventory
    await action.common_actions.show_character(game_user_id)
    await action.common_actions.show_inventory(game_user_id)

    await loop.run_wait_loop(5)
    await _send_counters(shared_state.RESOURCE_COUNTERS, shared_state.CHARACTER_NAME)
