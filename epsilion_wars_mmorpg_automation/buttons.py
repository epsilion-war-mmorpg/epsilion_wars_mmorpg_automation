"""Game buttons and utils."""

import itertools

from telethon import events, types

SEARCH_ENEMY = '⚔️ Найти врагов'
COMPLETE_BATTLE = '✅ Забрать нaграду'
RIP = '💀 Принять участь'
RUN_OUT_OF_BATTLE = 'Сбежать'
SKIP = 'Пропустить'
ATTACK_HEAD = 'В голову'


def get_buttons_flat(event: events.NewMessage.Event) -> list[types.TypeKeyboardButton]:
    """Get all available buttons from event message."""
    if not event.message.buttons:
        return []
    return list(itertools.chain(*event.message.buttons))