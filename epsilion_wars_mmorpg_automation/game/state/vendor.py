"""Random-vendor states."""

from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_random_vendor_meet(event: events.NewMessage.Event) -> bool:
    """Random vendor meet state."""
    # todo test
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False
    return 'странствующий торговец' in message and 'Покинуть' in found_buttons[-1].text


def is_random_vendor_meet_exit(event: events.NewMessage.Event) -> bool:
    """Random vendor exit state."""
    # todo test
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons or 'Войти в город' not in found_buttons[0].text:
        return False
    return 'ты покинул' in message or 'ты успешно купил' in message
