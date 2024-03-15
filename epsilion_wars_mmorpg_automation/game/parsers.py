"""Event message parsers."""
import base64
import re
from io import BytesIO
from math import ceil

from telethon import events, types

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.telegram_client import client

_turn_number_pattern = re.compile(r'ход\s+(\d+)')
_hp_level_pattern = re.compile(r'❤️\((\d+)/(\d+)\)')
_equip_hp_level_pattern = re.compile(r'\((\d+)/(\d+)\)')
_character_level_pattern = re.compile(r'(\d+)[\s]{0,}❤️\(\d+/\d+\)')
_character_name_pattern = re.compile(r'(.*\s🔸\d+)[\s]{0,}❤️\(\d+/\d+\)', re.MULTILINE | re.UNICODE)
_location_name_pattern = re.compile(r'(.{3,})\n\n.*', re.MULTILINE | re.UNICODE)
_experience_gain_pattern = re.compile(r'✨\sопыта:\s(\d+)')
_resource_counter_pattern = re.compile(r'(.*)\s-\s(\d+)шт', re.MULTILINE | re.UNICODE)
_potion_command_pattern = re.compile(r'(/\w+)', re.MULTILINE | re.UNICODE)
_scroll_command_pattern = re.compile(r'(/\w+)', re.MULTILINE | re.UNICODE)


def get_turn_number(message_content: str) -> int:
    """Return current turn number."""
    found = _turn_number_pattern.search(strip_message(message_content))
    if not found:
        return 0
    return int(found.group(1))


def get_hp_level(message_content: str) -> int:
    """Get current HP in percent."""
    current_level, max_level = get_character_hp(message_content)
    return ceil(int(current_level) / int(max_level) * 100)


def get_character_hp(message_content: str) -> tuple[int, int]:
    """Get character HP level."""
    found = _hp_level_pattern.search(strip_message(message_content), re.MULTILINE)
    if not found:
        raise InvalidMessageError('HP not found')

    current_level, max_level = found.group(1, 2)
    return int(current_level), int(max_level)


def get_equip_hp_level(message_content: str) -> int:
    """Get equip HP in absolute value."""
    found = _equip_hp_level_pattern.search(message_content)
    if not found:
        return 0
    return int(found.group(1))


def get_equip_hp_max_level(message_content: str) -> int:
    """Get equip HP max in absolute value."""
    found = _equip_hp_level_pattern.search(message_content)
    if not found:
        return 0
    return int(found.group(2))


def get_character_level(message_content: str) -> int:
    """Get character level."""
    found = _character_level_pattern.search(strip_message(message_content), re.MULTILINE)
    if not found:
        raise InvalidMessageError('Level not found')

    return int(found.group(1))


def get_character_name(message_content: str) -> str:
    """Get character name."""
    found = _character_name_pattern.search(message_content)
    if not found:
        raise InvalidMessageError('Character name not found')

    return found.group(1).strip()


def get_location_name(message_content: str) -> str:
    """Get location name."""
    found = _location_name_pattern.search(message_content)
    if not found:
        raise InvalidMessageError('Location name not found')

    return found.group(1)


def get_experience_gain(message_content: str) -> int:
    """Get battle experience gain amount."""
    found = _experience_gain_pattern.search(strip_message(message_content), re.MULTILINE)
    if not found:
        return 0
    return int(found.group(1))


def strip_message(original_message: str) -> str:
    """Return message content without EOL symbols."""
    return original_message.replace('\n', ' ').strip().lower()


async def get_photo_base64(event: events.NewMessage.Event) -> str | None:
    """Return message photo as base64 decoded string."""
    image_bytes = BytesIO()
    await client.download_media(
        message=event.message,
        file=image_bytes,
        thumb=-1,
    )
    image_str_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
    return image_str_base64.replace('data:image/png;', '').replace('base64,', '')


def get_resource_counters(original_message: str) -> dict[str, int]:
    """Return resource and amount in inventory."""
    message_with_fixes = original_message.replace(
        '📄 Рецепт',
        '📄Рецепт',
    )
    return {
        title: int(amount)
        for title, amount in _resource_counter_pattern.findall(message_with_fixes)
    }


def get_city_buttons(
    buttons: list[types.TypeKeyboardButton],
    names_filter: list[str] | None = None,
) -> list[types.TypeKeyboardButton]:
    """Return city buttons."""
    town_buttons = [
        button
        for button in buttons
        if '🏛' in button.text
    ]
    if not names_filter:
        return town_buttons

    filtered_buttons = []
    for button in town_buttons:
        for name in names_filter:
            if name.lower() in button.text.strip().lower():
                filtered_buttons.append(button)
                break
    return filtered_buttons


def get_potions(original_message: str) -> list[str]:
    """Return available potion commands."""
    return list(_potion_command_pattern.findall(original_message))


def get_scrolls(original_message: str) -> list[str]:
    """Return available scrolls commands."""
    return list(_scroll_command_pattern.findall(original_message))
