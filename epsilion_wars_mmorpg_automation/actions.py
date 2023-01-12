"""In-game actions."""

import logging
import random

from telethon import events

from epsilion_wars_mmorpg_automation.buttons import SEARCH_ENEMY, get_buttons_flat
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.message_parsers import parsers
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
    option = get_buttons_flat(event)[-1]
    logging.info('call complete battle command (%s)', option.text)

    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=option.text,
    )


async def ping(entity: int | events.NewMessage.Event) -> None:
    """Random short message for update current location state."""
    logging.info('call ping command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

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

    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=options[0].text,
    )


async def healing(event: events.NewMessage.Event) -> None:
    """Try to use heal pots if needed."""
    logging.info('call healing command')

    message_content = parsers.strip_message(event.message.message)
    hp_level_percent = parsers.get_hp_level(message_content)
    character_level = parsers.get_character_level(message_content)
    logging.info('HP and character level is [%d%%; %d]', hp_level_percent, character_level)

    if character_level >= app_settings.character_high_level_threshold:
        logging.warning('skip heal for high-levels characters')
        return

    if hp_level_percent <= app_settings.hp_level_for_mid_heal_pot:
        command = '/use_middle_hp'
    elif hp_level_percent < app_settings.hp_level_for_low_heal_pot:
        command = '/use_low_hp'
    else:
        logging.info('skip heal by HP level')
        return

    if character_level >= app_settings.character_middle_level_threshold:
        command = f'{command}II'

    await wait_for(1, 2)
    await client.send_message(
        entity=event.chat_id,
        message=command,
    )
