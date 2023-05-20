"""Hunting handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.game import action, state


async def hunting_start(event: events.NewMessage.Event) -> None:
    """Start hunt."""
    logging.info('start hunting event')
    response = await action.hunting_actions.select_hunt_type(event)
    if response:
        logging.info(f'{response.message=}')
        if state.hunting_states.is_bow_equip_needed(response.message):
            await action.common_actions.show_equip(event)


async def hunting_end(event: events.NewMessage.Event) -> None:
    """Restart hunt after end."""
    logging.info('end hunting event')
    await action.hunting_actions.complete_hunting(event)
    await action.hunting_actions.start_hunt(event.chat_id)
