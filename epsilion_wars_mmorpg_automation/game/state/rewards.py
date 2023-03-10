"""Rewards states."""
from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat, DAILY_REWARD_NOT_FOUND, DAILY_REWARD_FOUND


def is_daily_reward_not_found(event: events.NewMessage.Event) -> bool:
    """Daily rewards not found."""
    # todo test
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return found_buttons[0].text == DAILY_REWARD_NOT_FOUND


def is_daily_reward_found(event: events.NewMessage.Event) -> bool:
    """Daily rewards found."""
    # todo test
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return found_buttons[0].text == DAILY_REWARD_FOUND
