"""Game-specific captcha resolver."""
from typing import Any

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import capitalize_by_question, replace_eng_chars

_question_answer = {
    'столицаэпсилиона': 'Мелидон',
}


async def game_specific(message: str, *_: Any) -> str | None:
    """Resolve game-specific captcha."""
    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    question = replace_eng_chars(question)
    for question_pattern, answer in _question_answer.items():
        if question_pattern in question:
            return capitalize_by_question(answer, question)
    return None
