"""Numbers from image captcha resolver."""

import logging

from telethon import events

from epsilion_wars_mmorpg_automation.captcha import anti_captcha_provider
from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import replace_eng_chars
from epsilion_wars_mmorpg_automation.parsers.parsers import get_photo_base64

_common_pattern = 'отправьчислоскартинки'


async def image_with_numbers(message: str, event: events.NewMessage.Event) -> str | None:
    """Resolve image captcha by 3th-party service."""
    if not event.message.media:
        return None

    question = replace_eng_chars(
        source=message.lower().replace(' ', ''),
    )
    if _common_pattern not in question:
        return None

    image_source = await get_photo_base64(event)
    if not image_source:
        logging.warning(f'captcha event - image not found! "{image_source}"')
        return None

    return await anti_captcha_provider.resolve_image_to_number(image_source)
