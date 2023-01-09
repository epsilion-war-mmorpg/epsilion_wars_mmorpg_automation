import logging

from telethon import events

from app.buttons import SEARCH_ENEMY, COMPLETE_BATTLE
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
