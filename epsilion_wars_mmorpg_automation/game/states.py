"""Check event states."""


from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import (
    ATTACK_HEAD,
    COMPLETE_BATTLE,
    RIP,
    RUN_OUT_OF_BATTLE,
    SKIP,
    TO_HUNTING_ZONE,
    TO_TOWN,
    get_buttons_flat,
)
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_died_state(event: events.NewMessage.Event) -> bool:
    """U died state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) == 1 and found_buttons[0].text == RIP:
        return True

    if _is_battle_escape_try(event):
        return found_buttons[0].text == TO_TOWN

    message_content = strip_message(event.message.message)
    patterns = [
        'отправляешься в ближайший город на восстановление',
        'был отправлен восстанавливаться в город',
    ]
    return any([
        pattern in message_content
        for pattern in patterns
    ])


def is_selector_defence_direction(event: events.NewMessage.Event) -> bool:
    """Select defence."""
    return 'что будешь блокировать?' in strip_message(event.message.message)


def is_selector_attack_direction(event: events.NewMessage.Event) -> bool:
    """Select attack."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 6:
        return False

    if _is_already_ended_battle(event):
        return False

    message_content = event.message.message.strip()
    patterns = [
        'Куда будешь бить?',
        'Ход',
        'Куда бить?',
    ]
    is_message_valid = any([
        pattern in message_content for pattern in patterns
    ])
    if not is_message_valid:
        return False

    return found_buttons[5].text == RUN_OUT_OF_BATTLE and found_buttons[0].text == ATTACK_HEAD


def is_selector_combo(event: events.NewMessage.Event) -> bool:
    """Select combo-bite."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) < 3:
        return False

    if _is_already_ended_battle(event):
        return False

    last_buttons_text = [button.text for button in found_buttons[-2:]]
    return last_buttons_text == [SKIP, RUN_OUT_OF_BATTLE]


def is_win_state(event: events.NewMessage.Event) -> bool:
    """U win state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False

    if _is_battle_escape_try(event):
        return found_buttons[0].text == TO_HUNTING_ZONE

    return found_buttons[0].text == COMPLETE_BATTLE


def is_hunting_ready_state(event: events.NewMessage.Event) -> bool:
    """Ready for hunt state."""
    message = strip_message(event.message.message)
    if 'тюрьма' in message:
        return False
    if 'монстров пока нет' in message:
        return False
    return 'в локации можно встретить врагов.' in message


def _is_already_ended_battle(event: events.NewMessage.Event) -> bool:
    """Last turn of ended battle."""
    message_content = event.message.message.strip()
    return 'Ход' in message_content and '(0/' in message_content


def _is_battle_escape_try(event: events.NewMessage.Event) -> bool:
    message = strip_message(event.message.message)
    return 'попытался сбежать от' in message and 'попытка была провалена' in message
