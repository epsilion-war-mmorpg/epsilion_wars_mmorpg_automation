"""In-game actions."""

import logging
import random

from telethon import events

from epsilion_wars_mmorpg_automation.buttons import COMPLETE_BATTLE, SEARCH_ENEMY, get_buttons_flat
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def search_enemy(event: events.NewMessage.Event) -> None:
    """Start searching enemy."""
    logging.info('call search enemy command')
    await wait_for(3, 8)
    await client.send_message(
        entity=event.chat_id,
        message=SEARCH_ENEMY,
    )


async def complete_battle(event: events.NewMessage.Event) -> None:
    """Get rewards after battle."""
    logging.info('call complete battle command')
    await wait_for(1, 1)
    await client.send_message(
        entity=event.chat_id,
        message=COMPLETE_BATTLE,
    )


async def ping(game_bot_id: int) -> None:
    """Random short message for update current location state."""
    logging.info('call ping command')
    await client.send_message(
        entity=game_bot_id,
        message=app_settings.ping_message,
    )


async def select_defence_direction(event: events.NewMessage.Event) -> None:
    """Select defence direction."""
    logging.info('call select defence command')
    options = get_buttons_flat(event)[:5]
    logging.debug('defence options %s', options)
    if not options:
        raise InvalidMessageError('Defence selector buttons not found.')

    select = random.choice(options)
    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )


async def select_attack_direction(event: events.NewMessage.Event) -> None:
    """Select attack direction."""
    logging.info('call select attack command')
    options = get_buttons_flat(event)[:5]
    logging.debug('attack options %s', options)
    if not options:
        raise InvalidMessageError('Attack selector buttons not found.')

    select = random.choice(options)
    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )


async def select_combo(event: events.NewMessage.Event) -> None:
    """Select combo block."""
    logging.info('call select combo command')
    options = get_buttons_flat(event)[:-2]
    logging.debug('combo options %s', options)
    if not options:
        raise InvalidMessageError('Combo selector buttons not found.')

    select = random.choice(options)
    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )
