"""Captcha resolve methods."""

from dataclasses import dataclass
from typing import Callable

from telethon import events

from epsilion_wars_mmorpg_automation.captcha.game_specific import game_specific
from epsilion_wars_mmorpg_automation.captcha.image_with_numbers import image_with_numbers
from epsilion_wars_mmorpg_automation.captcha.simple_emoji import simple_emoji
from epsilion_wars_mmorpg_automation.captcha.simple_grammar import simple_grammar
from epsilion_wars_mmorpg_automation.captcha.simple_math import simple_math
from epsilion_wars_mmorpg_automation.settings import app_settings


@dataclass
class CaptchaAnswer:
    """Captcha answer type."""

    resolver_type: str
    question: str
    answer: str | None = None


async def try_resolve(event: events.NewMessage.Event) -> CaptchaAnswer:
    """Try to resolve captcha."""
    resolvers_enabled: list[Callable] = [
        game_specific,
        simple_math,
        simple_emoji,
        simple_grammar,
    ]

    if app_settings.anti_captcha_com_apikey:
        resolvers_enabled.append(image_with_numbers)

    for resolver in resolvers_enabled:
        answer_str = await resolver(event.message.message, event)
        if answer_str:
            return CaptchaAnswer(
                resolver_type=resolver.__name__,
                question=event.message.message,
                answer=answer_str,
            )

    return CaptchaAnswer(resolver_type='', question=event.message.message, answer=None)
