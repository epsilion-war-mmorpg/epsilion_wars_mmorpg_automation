"""Emoji-captcha resolver."""
from typing import Any

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import capitalize_by_question, replace_eng_chars

_common_pattern = 'название'
_question_answer = {
    '🧟‍♂': 'орки',
    '🧝‍♂️': 'эльфы',
    '🧝‍♀️': 'эльфы',
    '🤴️': 'люди',
    '👸️': 'люди',
    '🐺': 'волк',
    '🤡': 'клоун',
    '🍌': 'банан',
    '⚽': 'футбол',
    '💩': 'аниме',
    '🍕': 'пицца',
}


async def simple_emoji(message: str, *_: Any) -> str | None:
    """Resolve emoji text captcha."""
    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    question = replace_eng_chars(question)
    if _common_pattern not in question:
        return None

    for emoji, answer in _question_answer.items():
        if emoji in question:
            return capitalize_by_question(answer, question)
    return None
