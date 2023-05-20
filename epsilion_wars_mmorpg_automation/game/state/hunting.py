"""Hunting states."""
from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_hunting_type_selector(event: events.NewMessage.Event) -> bool:
    """Select hunt type."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    return 'на охоте можно добыть свежего мяса' in message and len(found_buttons) == 2


def is_equip_bow_state(event: events.NewMessage.Event) -> bool:
    """Approve bow equip request."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return 'позволяет отправляться на охоту' in message and 'Надеть' in found_buttons[0].text


def is_hunting_end(event: events.NewMessage.Event) -> bool:
    """Complete hunt state."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return 'охота сегодня была особенно удачна' in message

    return '🏹 Охота завершена' in message and 'Вернуться в локацию' in found_buttons[0].text


def is_bow_equip_needed(message: str) -> bool:
    """Hunting-compatible bow not equipped."""
    if 'нужно надеть охотничий лук' in strip_message(message):
        return True
    return 'недостаточно прочности' in strip_message(message)
