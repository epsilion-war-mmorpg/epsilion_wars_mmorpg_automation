"""Event message parsers."""
import base64
import re
from io import BytesIO
from math import ceil

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.telegram_client import client

_hp_level_pattern = re.compile(r'❤️\((\d+)/(\d+)\)')
_equip_hp_level_pattern = re.compile(r'\((\d+)/\d+\)')
_character_level_pattern = re.compile(r'(\d+)[\s]{0,}❤️\(\d+/\d+\)')
_character_name_pattern = re.compile(r'(.*\s🔸\d+)[\s]{0,}❤️\(\d+/\d+\)', re.MULTILINE | re.UNICODE)
_location_name_pattern = re.compile(r'(.{3,})\n\n.*', re.MULTILINE | re.UNICODE)
_experience_gain_pattern = re.compile(r'✨\sопыта:\s(\d+)')
_resource_counter_pattern = re.compile(r'(.*)\s-\s(\d+)шт', re.MULTILINE | re.UNICODE)


def get_hp_level(message_content: str) -> int:
    """Get current HP in percent."""
    found = _hp_level_pattern.search(strip_message(message_content), re.MULTILINE)
    if not found:
        raise InvalidMessageError('HP not found')

    current_level, max_level = found.group(1, 2)
    return ceil(int(current_level) / int(max_level) * 100)


def get_equip_hp_level(message_content: str) -> int:
    """Get equip HP in absolute value."""
    found = _equip_hp_level_pattern.search(message_content)
    if not found:
        return 0
    return int(found.group(1))


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

    return found.group(1)


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
