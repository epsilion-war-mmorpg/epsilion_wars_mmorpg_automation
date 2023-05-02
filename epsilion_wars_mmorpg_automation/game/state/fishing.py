"""Fishing states."""
from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_fishing_type_selector(event: events.NewMessage.Event) -> bool:
    """Select fishing type."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    return 'в некоторых водоемах можно рыбачить рыбу' in message and len(found_buttons) == 2


def is_equip_rod_state(event: events.NewMessage.Event) -> bool:
    """Approve rod equip request."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return 'позволяет участвовать в рыбалке' in message and 'Надеть' in found_buttons[0].text


def is_fishing_end(event: events.NewMessage.Event) -> bool:
    """Complete fishing state."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return 'ловля рыбы сегодня была особенно удачна' in message

    return '🎣️ рыбалка завершена' in message and 'Вернуться в локацию' in found_buttons[0].text


def is_rod_equip_needed(message: str) -> bool:
    """Fishing-compatible rod not equipped."""
    if 'нужно надеть удочку' in strip_message(message):
        return True
    return 'недостаточно прочности у удочки' in strip_message(message)
