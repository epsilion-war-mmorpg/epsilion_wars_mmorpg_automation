"""Actions for farming."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def go_to_town(event: events.NewMessage.Event) -> None:
    """Go to town."""
    town_options = get_buttons_flat(event)
    logging.debug('town options %s', town_options)

    if not town_options:
        raise InvalidMessageError('Town selector buttons not found.')

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=town_options[0].text,
    )
