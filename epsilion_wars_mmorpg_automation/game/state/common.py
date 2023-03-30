"""Check messages by patterns."""


from telethon import events

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.game.parsers import strip_message


def is_equip_broken_message(event: events.NewMessage.Event) -> bool:
    """Equip broken message."""
    message = strip_message(event.message.message)
    return 'экипировка' in message and 'снята из-за поломки' in message


def is_hp_updated_message(event: events.NewMessage.Event) -> bool:
    """HP updated message."""
    message = strip_message(event.message.message)
    patterns = {
        'ваше здоровье полностью восстановлено',
        'ваше здоровье восстановлено',
        'ед. здоровья. текущее здоровье:',  # after success use heal pot
    }
    for pattern in patterns:
        if pattern in message:
            return True
    return False


def is_captcha_message(event: events.NewMessage.Event) -> bool:
    """Captcha shot."""
    return 'ты встретил капчу' in strip_message(event.message.message)


def is_character_equip_select(event: events.NewMessage.Event) -> bool:
    """Character equip state."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) not in {8, 9}:
        return False

    return 'надетая экипировка:' in message and 'Оружие' in found_buttons[0].text


def is_character_equip_gun_select(event: events.NewMessage.Event) -> bool:
    """Character equip state."""
    message = strip_message(event.message.message)
    found_buttons = get_buttons_flat(event)
    if not found_buttons:
        return False

    if is_character_equip_select(event):
        return False

    last_button = found_buttons[-1]
    first_button = found_buttons[0]

    return 'надетая экипировка:' in message and 'Назад' in last_button.text and '🔪' in first_button.text
