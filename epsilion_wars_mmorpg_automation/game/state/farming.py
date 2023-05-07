"""Farming states."""


from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import REPAIR, get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_repair_button_available(event: events.NewMessage.Event) -> bool:
    """Found "repair" button in dialog options."""
    found_buttons = get_buttons_flat(event)
    return any(REPAIR in button.text for button in found_buttons)


def is_repair_item_selector(event: events.NewMessage.Event) -> bool:
    """Is "select item for repair" dialog."""
    message = strip_message(event.message.message)
    return 'что хочешь отремонтировать?' in message or 'тебе не требуется ремонт' in message


def is_repair_item_approve_request(event: events.NewMessage.Event) -> bool:
    """Is "approve item repair request" dialog."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 2:
        return False
    return 'починить' in message and 'отремонтировать' in found_buttons[0].text.lower()
