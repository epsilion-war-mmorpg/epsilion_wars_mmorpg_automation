import logging
import random

from telethon import events

from app.buttons import COMPLETE_BATTLE, SEARCH_ENEMY, get_buttons_flat
from app.exceptions import InvalidMessageError
from app.telegram_client import client


async def search_enemy(event: events.NewMessage.Event) -> None:
    logging.info('call search enemy command')
    # todo throttling
    await client.send_message(
        entity=event.chat_id,
        message=SEARCH_ENEMY,
    )


async def complete_battle(event: events.NewMessage.Event) -> None:
    logging.info('call complete battle command')
    # todo throttling
    await client.send_message(
        entity=event.chat_id,
        message=COMPLETE_BATTLE,
    )


async def ping(game_bot_id: int) -> None:
    logging.info('call ping command')
    # todo throttling
    await client.send_message(
        entity=game_bot_id,
        message='/me',
    )


async def select_defence_direction(event: events.NewMessage.Event) -> None:
    logging.info('call select defence command')
    # todo throttling
    options = get_buttons_flat(event)[:5]
    logging.debug('defence options %s', options)
    if not options:
        raise InvalidMessageError('Defence selector buttons not found.')

    select = random.choice(options)
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )


async def select_attack_direction(event: events.NewMessage.Event) -> None:
    logging.info('call select attack command')
    # todo throttling
    options = get_buttons_flat(event)[:5]
    logging.debug('attack options %s', options)
    if not options:
        raise InvalidMessageError('Attack selector buttons not found.')

    select = random.choice(options)
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )