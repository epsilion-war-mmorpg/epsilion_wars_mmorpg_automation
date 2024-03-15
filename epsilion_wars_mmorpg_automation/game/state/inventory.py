"""Rewards states."""
from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import NEXT_PAGE_BUTTON, get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def has_show_next_page_button(event: events.NewMessage.Event) -> bool:
    """Pagination with "next page" button."""
    if not is_resource_pagination(event):
        return False
    found_buttons = {button.text for button in get_buttons_flat(event)}
    return NEXT_PAGE_BUTTON in found_buttons


def is_resource_type_selector(event: events.NewMessage.Event) -> bool:
    """Select resource type state."""
    message = strip_message(event.message.message)
    if not get_buttons_flat(event):
        return False
    return '♻️ ресурсы' in message and 'ресурсы обычно используются для крафта' in message


def is_resource_pagination(event: events.NewMessage.Event) -> bool:
    """Pagination with "next page" button."""
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False
    return 'К ресурсам' in found_buttons[-1].text


def is_potions_selector(event: events.NewMessage.Event) -> bool:
    """Is a potion list."""
    message = strip_message(event.message.message)
    return '🧪 зелья' in message


def is_scrolls_selector(event: events.NewMessage.Event) -> bool:
    """Is a scrolls list."""
    message = strip_message(event.message.message)
    return '📃 свитки' in message
