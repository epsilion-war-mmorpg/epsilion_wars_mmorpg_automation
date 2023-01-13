"""Check event states."""

from telethon import events

from epsilion_wars_mmorpg_automation.buttons import (
    ATTACK_HEAD,
    COMPLETE_BATTLE,
    RIP,
    RUN_OUT_OF_BATTLE,
    SKIP,
    get_buttons_flat,
)


def is_hunting_ready_message(event: events.NewMessage.Event) -> bool:
    """Ready for hunt."""
    return 'можно встретить врагов' in event.message.message.strip().lower()


def is_equip_broken_message(event: events.NewMessage.Event) -> bool:
    """Equip broken message."""
    message = event.message.message.strip().lower()
    return 'экипировка' in message and 'снята из-за поломки' in message


def is_hp_updated_message(event: events.NewMessage.Event) -> bool:
    """HP updated message."""
    message = event.message.message.strip().lower()
    patterns = {
        'ваше здоровье полностью восстановлено',
        'ваше здоровье восстановлено',
        'ед. здоровья. текущее здоровье:',  # after success use heal pot
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False


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

    if _is_already_ended_turn(event):
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

    if _is_already_ended_turn(event):
        return False

    last_buttons_text = [button.text for button in found_buttons[-2:]]
    return last_buttons_text == [SKIP, RUN_OUT_OF_BATTLE]


def is_win_state(event: events.NewMessage.Event) -> bool:
    """U win state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == COMPLETE_BATTLE


def is_captcha_state(event: events.NewMessage.Event) -> bool:
    """Captcha shot."""
    message_content = event.message.message.strip()
    return 'ты встретил капчу' in message_content


def _is_already_ended_turn(event: events.NewMessage.Event) -> bool:
    """Last turn of ended battle."""
    message_content = event.message.message.strip()
    return 'Ход' in message_content and '(0/' in message_content
