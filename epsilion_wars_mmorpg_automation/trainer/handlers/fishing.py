"""Fishing handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.game import action, state


async def fishing_start(event: events.NewMessage.Event) -> None:
    """Start fishing."""
    logging.info('start fishing event')
    response = await action.fishing_actions.select_fishing_type(event)
    if response:
        logging.info(f'{response.message}')
        if state.fishing_states.is_rod_equip_needed(response.message):
            await action.common_actions.show_equip(event)


async def fishing_end(event: events.NewMessage.Event) -> None:
    """Restart fishing after end."""
    logging.info('end fishing event')
    await action.fishing_actions.complete_fishing(event)
    await action.fishing_actions.start_fishing(event.chat_id)
