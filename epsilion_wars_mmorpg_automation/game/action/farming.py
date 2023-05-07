"""Actions for farming."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def go_to(event: events.NewMessage.Event, direction: str) -> None:
    """Go to action."""
    go_to_options = get_buttons_flat(event)
    logging.info('go to call %s', go_to_options)

    if not go_to_options:
        raise InvalidMessageError('Go to selector buttons not found.')

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=direction,
    )
