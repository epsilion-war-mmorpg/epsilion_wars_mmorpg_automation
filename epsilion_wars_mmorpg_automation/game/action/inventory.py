"""Actions with inventory."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import shared_state
from epsilion_wars_mmorpg_automation.game.buttons import NEXT_PAGE_BUTTON, get_buttons_flat, get_resource_button
from epsilion_wars_mmorpg_automation.game.parsers import get_character_name
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def show_resource_type(event: events.NewMessage.Event) -> None:
    """Call show resources."""
    resource = get_resource_button(shared_state.RESOURCE_TYPE)
    logging.info(f'show resources "{resource}"')
    if not resource:
        raise RuntimeError('Invalid resource type requested.')

    for index, inline_button in enumerate(get_buttons_flat(event)):
        if resource in inline_button.text:
            await wait_for()
            await event.message.click(index)
            return


async def show_next_page(event: events.NewMessage.Event) -> None:
    """Click next page."""
    logging.info('show next page button')
    for index, inline_button in enumerate(get_buttons_flat(event)):
        if inline_button.text == NEXT_PAGE_BUTTON:
            await wait_for()
            await event.message.click(index)


async def save_character_name(event: events.NewMessage.Event) -> None:
    """Get and save character name to shared state."""
    logging.info('save character nickname')
    shared_state.CHARACTER_NAME = get_character_name(event.message.message)
