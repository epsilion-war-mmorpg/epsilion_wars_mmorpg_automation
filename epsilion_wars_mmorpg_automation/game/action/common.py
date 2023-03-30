"""Common game actions."""
import logging
import random

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import EQUIP, get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def ping(entity: int | events.NewMessage.Event) -> None:
    """Random short message for update current location state."""
    logging.info('call ping command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    message = random.choice(
        seq=app_settings.ping_commands,
    )
    logging.info(f'call ping command debug {game_bot_id=} {message=}')
    await client.send_message(
        entity=game_bot_id,
        message=message,
    )


async def captcha_answer(event: events.NewMessage.Event, answer: str) -> None:
    """Send captcha answer."""
    logging.info('call captcha answer command')

    await wait_for(4, 9)
    await client.send_message(
        entity=event.chat_id,
        message=answer,
    )


async def show_equip(event: events.NewMessage.Event) -> None:
    """Call show equip."""
    logging.info('call show equip button')
    await wait_for(1, 2)
    await client.send_message(
        entity=event.chat_id,
        message=EQUIP,
    )


async def show_equip_guns(event: events.NewMessage.Event) -> None:
    """Call select gun button."""
    logging.info('call select gun button')
    inline_buttons = get_buttons_flat(event)
    if len(inline_buttons) < 8:
        raise InvalidMessageError('Invalid equip buttons.')

    await wait_for(1, 2)
    await event.message.click(0)


async def equip_use(event: events.NewMessage.Event) -> None:
    """Call use selected equip."""
    logging.info('call use selected equip')
    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Invalid equip buttons.')

    await wait_for(1, 2)
    await event.message.click(0)
