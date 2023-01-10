"""Check event states."""

from telethon import events

from app.buttons import ATTACK_HEAD, COMPLETE_BATTLE, RIP, RUN_OUT_OF_BATTLE, get_buttons_flat


def is_hunting_ready_message(event: events.NewMessage.Event) -> bool:
    """Ready for hunt."""
    return 'можно встретить врагов' in event.message.message.strip().lower()


def is_hp_full_message(event: events.NewMessage.Event) -> bool:
    """HP is full message."""
    return 'ваше здоровье полностью восстановлено' in event.message.message.strip().lower()


def is_died_state(event: events.NewMessage.Event) -> bool:
    """U died state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == RIP


def is_selector_defence_direction(event: events.NewMessage.Event) -> bool:
    """Select defence."""
    return 'что будешь блокировать?' in event.message.message.strip().lower()


def is_selector_attack_direction(event: events.NewMessage.Event) -> bool:
    """Select attack."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 6:
        return False
    return found_buttons[5].text == RUN_OUT_OF_BATTLE and found_buttons[0].text == ATTACK_HEAD


def is_win_state(event: events.NewMessage.Event) -> bool:
    """U win state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == COMPLETE_BATTLE
