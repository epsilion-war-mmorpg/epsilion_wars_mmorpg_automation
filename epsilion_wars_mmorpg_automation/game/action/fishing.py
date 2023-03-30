"""Actions with fishing."""
import logging

from telethon import events
from telethon.tl.types.messages import BotCallbackAnswer

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import FISHING, get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import get_equip_hp_level
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def start_fishing(game_bot_id: int) -> None:
    """Call start fishing."""
    logging.info('call start fishing button')
    await wait_for(1, 2)
    await client.send_message(
        entity=game_bot_id,
        message=FISHING,
    )


async def select_fishing_type(event: events.NewMessage.Event) -> BotCallbackAnswer:
    """Select fishing type."""
    logging.info('select fishing type')
    inline_buttons = get_buttons_flat(event)
    if len(inline_buttons) != 2:
        raise InvalidMessageError('Invalid fishing-type buttons.')

    await wait_for(1, 2)
    return await event.message.click(1)


async def equip_rod(event: events.NewMessage.Event) -> None:
    """Select fishing-rod as gun and equip it."""
    logging.info('equip rod if possible')
    rods = [
        (index, button.text, get_equip_hp_level(button.text))
        for index, button in enumerate(get_buttons_flat(event))
        if 'Удочка' in button.text
    ]
    logging.info(f'found rods {rods}')
    compatible_rods = [
        rod
        for rod in rods
        if rod[2] >= app_settings.rod_minimal_hp_level_for_fishing
    ]
    logging.info(f'found compatible rods {compatible_rods}')
    if not compatible_rods:
        logging.warning('not found rods')
        return

    selected_rod = compatible_rods[-1]
    if '✅' in selected_rod[1]:
        logging.info('already equipped')
        return

    await wait_for(1, 2)
    await event.message.click(selected_rod[0])


async def complete_fishing(event: events.NewMessage.Event) -> None:
    """Get rewards after fishing."""
    logging.info('call complete fishing command')

    options = get_buttons_flat(event)
    if not options:
        raise InvalidMessageError('Invalid fishing complete buttons.')

    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=options[0].text,
    )
