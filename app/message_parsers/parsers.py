"""Event message parsers."""

import re
from math import ceil

from app.exceptions import InvalidMessageError

_hp_level_pattern = re.compile(r'❤️\((\d+)/(\d+)\)')


def get_hp_level(message_content: str) -> int:
    """Get current HP in percent."""
    found = _hp_level_pattern.search(message_content.strip(), re.MULTILINE)
    if not found:
        raise InvalidMessageError('HP not found')

    current_level, max_level = found.group(1, 2)
    return ceil(int(current_level) / int(max_level) * 100)


def strip_message(original_message: str) -> str:
    """Return message content without EOL symbols."""
    return original_message.strip().replace('\n', ' ')
