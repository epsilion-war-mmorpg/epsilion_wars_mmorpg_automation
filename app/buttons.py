import itertools

from telethon import events, types

SEARCH_ENEMY = '⚔️ Найти врагов'
COMPLETE_BATTLE = '✅ Забрать нaграду'
RIP = '💀 Принять участь'
RUN_OUT_OF_BATTLE = 'Сбежать'
ATTACK_HEAD = 'В голову'


def get_buttons_flat(event: events.NewMessage.Event) -> list[types.TypeKeyboardButton]:
    if not event.message.buttons:
        return []
    return list(itertools.chain(*event.message.buttons))
