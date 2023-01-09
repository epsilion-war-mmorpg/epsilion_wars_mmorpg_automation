import re
from math import ceil

from telethon import events

_hp_level_pattern = re.compile(r'❤️\((\d+)/(\d+)\)\n')


class UnprocessableMessage(Exception):
    pass


class InvalidMessageHP(UnprocessableMessage):
    pass


def is_hunting_ready_message(message_content: str) -> bool:
    return 'можно встретить врагов' in message_content.strip().lower()


def is_died_state(event: events.NewMessage.Event) -> bool:
    if event.message.button_count != 1:
        return False
    return event.message.buttons[0][0].text == '💀 Принять участь'


def parse_hp_level(message_content: str) -> int:
    found = _hp_level_pattern.search(message_content.strip(), re.MULTILINE)
    if not found:
        raise InvalidMessageHP()

    current_level, max_level = found.group(1, 2)
    return ceil(int(current_level) / int(max_level) * 100)


