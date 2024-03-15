"""Common game actions."""
import logging
import random

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import CHARACTER, EQUIP, INVENTORY, MAP, get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import WaitActions, wait_for


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
    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=message,
    )


async def captcha_answer(event: events.NewMessage.Event, answer: str) -> None:
    """Send captcha answer."""
    logging.info('call captcha answer command')

    await wait_for(WaitActions.CAPTCHA)
    await client.send_message(
        entity=event.chat_id,
        message=answer,
    )


async def show_equip(event: events.NewMessage.Event) -> None:
    """Call show equip."""
    logging.info('call show equip button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=EQUIP,
    )


async def show_map(event: events.NewMessage.Event) -> None:
    """Call show map."""
    logging.info('call show map button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=MAP,
    )


async def show_npc(event: events.NewMessage.Event) -> None:
    """Call show NPC."""
    logging.info('call show NPC button')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message='/npc',
    )


async def call_npc(event: events.NewMessage.Event, name: str) -> None:
    """Call NPC."""
    logging.info('call NPC')
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=name,
    )


async def call_binding(event: events.NewMessage.Event, binding_number: int) -> None:
    """Call saved binding."""
    logging.info('call binding {0}'.format(binding_number))
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=str(binding_number),
    )


async def show_inventory(entity: int | events.NewMessage.Event) -> None:
    """Call show inventory."""
    logging.info('call show inventory button')
    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=INVENTORY,
    )


async def show_character(entity: int | events.NewMessage.Event) -> None:
    """Call show character."""
    logging.info('call show character button')
    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=CHARACTER,
    )


async def show_equip_guns(event: events.NewMessage.Event) -> None:
    """Call select gun button."""
    logging.info('call select gun button')
    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Invalid equip buttons.')

    await wait_for()
    await event.message.click(0)


async def exit_after_vendor(event: events.NewMessage.Event) -> None:
    """Exit after vendor meet."""
    logging.info('call exit after vendor dialog')
    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Invalid vendor buttons.')

    await wait_for()
    await event.message.click(0)


async def execute_command(entity: int, command: str) -> None:
    """Execute custom command."""
    logging.info('call command execution {0}'.format(command))
    await wait_for()
    await client.send_message(
        entity=entity,
        message=command,
    )


async def show_potions(entity: int | events.NewMessage.Event) -> None:
    """Call show potions."""
    logging.info('call show potions command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    await execute_command(
        entity=game_bot_id,
        command='/potion',
    )


async def show_scrolls(entity: int | events.NewMessage.Event) -> None:
    """Call show scrolls."""
    logging.info('call show scrolls command')

    if isinstance(entity, events.NewMessage.Event):
        game_bot_id = entity.chat_id
    else:
        game_bot_id = entity

    await execute_command(
        entity=game_bot_id,
        command='/свитки',
    )
