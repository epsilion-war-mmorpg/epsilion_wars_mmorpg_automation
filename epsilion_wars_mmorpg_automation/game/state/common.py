"""Check messages by patterns."""


from telethon import events

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
