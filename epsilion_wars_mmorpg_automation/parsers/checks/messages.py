"""Check messages by patterns."""


from telethon import events


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


def is_captcha_message(event: events.NewMessage.Event) -> bool:
    """Captcha shot."""
    message_content = event.message.message.strip()
    return 'ты встретил капчу' in message_content
