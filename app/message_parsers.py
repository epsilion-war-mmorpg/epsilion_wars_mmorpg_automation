import re
from math import ceil

from telethon import events

from app.buttons import ATTACK_HEAD, COMPLETE_BATTLE, RIP, RUN_OUT_OF_BATTLE, get_buttons_flat
from app.exceptions import InvalidMessageError

_hp_level_pattern = re.compile(r'❤️\((\d+)/(\d+)\)\n')


def is_hunting_ready_message(message_content: str) -> bool:
    return 'можно встретить врагов' in message_content.strip().lower()


def is_hp_full_message(message_content: str) -> bool:
    return 'ваше здоровье полностью восстановлено' in message_content.strip().lower()


def is_died_state(event: events.NewMessage.Event) -> bool:
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == RIP


def is_selector_defence_direction(event: events.NewMessage.Event) -> bool:
    return 'что будешь блокировать?' in event.message.message.strip().lower()


def is_selector_attack_direction(event: events.NewMessage.Event) -> bool:
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 6:
        return False
    return found_buttons[5].text == RUN_OUT_OF_BATTLE and found_buttons[0].text == ATTACK_HEAD


def is_win_state(event: events.NewMessage.Event) -> bool:
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == COMPLETE_BATTLE


def parse_hp_level(message_content: str) -> int:
    found = _hp_level_pattern.search(message_content.strip(), re.MULTILINE)
    if not found:
        raise InvalidMessageError('HP not found')

    current_level, max_level = found.group(1, 2)
    return ceil(int(current_level) / int(max_level) * 100)

