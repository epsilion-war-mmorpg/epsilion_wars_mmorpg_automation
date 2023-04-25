"""Farming states."""


from telethon import events

from epsilion_wars_mmorpg_automation.game import buttons
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_repairing_city_state(event: events.NewMessage.Event) -> bool:
    """Ready for repair start state."""

    # todo return current location is city
    # todo impl
    # todo test
    message = strip_message(event.message.message)
    if 'тюрьма' in message:
        return False
    if 'монстров пока нет' in message:
        return False

    found_buttons = buttons.get_buttons_flat(event)
    if len(found_buttons) < 2:
        return False

    return found_buttons[1].text == buttons.SEARCH_ENEMY
