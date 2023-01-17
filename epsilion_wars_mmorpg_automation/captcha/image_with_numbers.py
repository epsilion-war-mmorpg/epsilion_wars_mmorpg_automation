import re

from telethon import events

from epsilion_wars_mmorpg_automation.captcha import anti_captcha_provider
from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import replace_eng_chars

_common_pattern = 'отправьчислоскартинки'


async def image_with_numbers(message: str, event: events.NewMessage.Event) -> str | None:
    """Resolver image captcha by 3th-party service."""

    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    question = replace_eng_chars(question)
    if _common_pattern in question:
        return None

    image_source = 'todo'
    return await anti_captcha_provider.resolve_image_to_number(image_source)

