"""Game buttons and utils."""

import itertools

from telethon import events, types

SEARCH_ENEMY = '⚔️ Найти врагов'
REWARDS = '🎁 Награды'
FISHING = '🎣 Рыбалка'
EQUIP = '🎒 Экипировка'
MAP = '🗺 Карта'
CHARACTER = '🚩 Герой'
INVENTORY = '♻️ Ресурсы'
COMPLETE_BATTLE = '✅ Забрать нaграду'
RIP = '💀 Принять участь'
RUN_OUT_OF_BATTLE = 'Сбежать'
SKIP = 'Пропустить'
ATTACK_HEAD = 'В голову'
TO_HUNTING_ZONE = 'В зону охоты'
TO_TOWN = 'В город'
NEXT_PAGE_BUTTON = '➡️'
REPAIR = 'Ремонт'


def get_resource_button(resource_type: str) -> str | None:
    """Get resource button name by code."""
    return {
        'resource': 'Крафтовые',
        'receipt': 'Рецепты',
        'books': 'Книги навыков',
        'scroll': 'Свитки',
        'potion': 'Зелья',
        'other': 'Прочее',
    }.get(resource_type)


def get_buttons_flat(event: events.NewMessage.Event) -> list[types.TypeKeyboardButton]:
    """Get all available buttons from event message."""
    if not event.message.buttons:
        return []
    return list(itertools.chain(*event.message.buttons))
