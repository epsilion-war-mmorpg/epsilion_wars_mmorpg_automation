import logging

from telethon import events

from app.telegram_client import client


search_enemy_command = '⚔️ Найти врагов'


async def search_enemy_call(event: events.NewMessage.Event):
    logging.info('call search enemy command')
    # todo throotling
    await client.send_message(
        entity=event.chat_id,
        message=search_enemy_command,
    )
