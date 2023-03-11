"""Common game actions."""
import logging
import random

from telethon import events

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
        seq=',.-',
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
