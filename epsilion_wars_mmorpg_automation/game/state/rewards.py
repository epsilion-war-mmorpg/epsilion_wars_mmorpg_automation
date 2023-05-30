"""Rewards states."""
from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import MENU_BUTTON, get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_daily_reward_not_found(event: events.NewMessage.Event) -> bool:
    """Daily rewards not found."""
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return 'Ежедневная награда' in found_buttons[0].text and not is_daily_reward_found(event)


def is_daily_reward_found(event: events.NewMessage.Event) -> bool:
    """Daily rewards found."""
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    return 'Ежедневная награда' in found_buttons[0].text and '❗️' in found_buttons[0].text


def have_unread_message(event: events.NewMessage.Event) -> bool:
    """Menu button show unread message."""
    for button in get_buttons_flat(event):
        if MENU_BUTTON in button.text and '❗️' in button.text:
            return True
    return False


def is_reward_recipient_selector(event: events.NewMessage.Event) -> bool:
    """Select daily reward recipient."""
    message = strip_message(event.message.message)
    return 'твоя награда сегодня' in message and 'какому персонажу ее отправить?' in message


def is_reward_catch_message(event: events.NewMessage.Event) -> bool:
    """Daily rewards catch."""
    message = strip_message(event.message.message)
    return 'ежедневная награда' in message and 'твоя награда -' in message


def is_reward_already_used_message(event: events.NewMessage.Event) -> bool:
    """Daily rewards already used."""
    message = strip_message(event.message.message)
    return 'ты уже получил награду сегодня' in message
