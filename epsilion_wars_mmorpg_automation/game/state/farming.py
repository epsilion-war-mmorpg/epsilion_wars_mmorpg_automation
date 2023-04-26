"""Farming states."""


from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import REPAIR, get_buttons_flat


def is_repair_button_available(event: events.NewMessage.Event) -> bool:
    """Found "repair" button in dialog options."""
    # todo test
    found_buttons = get_buttons_flat(event)
    return any(REPAIR in button.text for button in found_buttons)
