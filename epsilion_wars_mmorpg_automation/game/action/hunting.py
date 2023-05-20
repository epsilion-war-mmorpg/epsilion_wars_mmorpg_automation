"""Actions with hunt."""
import logging

from telethon import events
from telethon.tl.types.messages import BotCallbackAnswer

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import HUNTING, get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import get_equip_hp_level
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def start_hunt(game_bot_id: int) -> None:
    """Call start hunt button."""
    logging.info('call start hunt button')
    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=HUNTING,
    )


async def select_hunt_type(event: events.NewMessage.Event) -> BotCallbackAnswer:
    """Select hunt type."""
    logging.info('select hunt type')
    inline_buttons = get_buttons_flat(event)
    if len(inline_buttons) != 2:
        raise InvalidMessageError('Invalid hunt-type buttons.')

    await wait_for()
    return await event.message.click(1)


async def equip_bow(event: events.NewMessage.Event) -> None:
    """Select hunting-bow as gun and equip it."""
    logging.info('equip bow if possible')
    bows = [
        (index, button.text, get_equip_hp_level(button.text))
        for index, button in enumerate(get_buttons_flat(event))
        if 'Лук' in button.text
    ]
    logging.info(f'found bows {bows}')
    compatible_bows = [
        bow
        for bow in bows
        if bow[2] >= app_settings.bow_minimal_hp_level_for_hunting
    ]
    logging.info(f'found compatible bows {compatible_bows}')
    if not compatible_bows:
        logging.warning('not found bows')
        return

    selected_bow = compatible_bows[-1]
    if '✅' in selected_bow[1]:
        logging.info('already equipped')
        return

    await wait_for()
    await event.message.click(selected_bow[0])


async def complete_hunting(event: events.NewMessage.Event) -> None:
    """Get rewards after hunting."""
    logging.info('call complete hunting command')

    options = get_buttons_flat(event)
    if not options:
        raise InvalidMessageError('Invalid hunting complete buttons.')

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=options[0].text,
    )


async def equip_use(event: events.NewMessage.Event) -> None:
    """Call use selected equip."""
    logging.info('call use selected equip')
    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Invalid equip buttons.')

    await wait_for()
    await event.message.click(0)
