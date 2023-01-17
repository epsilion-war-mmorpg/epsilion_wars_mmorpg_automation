"""Resolver for simple grammar operations captcha."""
import logging
import re
from typing import Any

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import capitalize_by_question, replace_eng_chars

_common_pattern = re.compile(r'(?P<question>[\wёЁ*]+)-напишитеправильно(месяц|слово)')
_old_generation_pattern = re.compile(r'(город)?(?P<question>[\wёЁ*]+)-напишитеответ')
_words = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',

    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',

    'кошка',
    'собака',
    'портрет',
    'колодец',
    'календарь',
    'сила',
    'ловкость',
    'интуиция',
    'выносливость',
    'скорость',
    'цирта',
]


async def simple_grammar(message: str, *_: Any) -> str | None:
    """Resolve simple grammar captcha."""
    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    question = replace_eng_chars(question)
    found = _common_pattern.search(question)
    if not found:
        found = _old_generation_pattern.search(question)

    if not found:
        return None

    found_word_pattern = found.group('question').replace('*', '.').strip().lower()
    found_word_pattern = replace_eng_chars(found_word_pattern)
    logging.debug(f'grammar captcha resolver: {found_word_pattern=}')

    for answer in _words:
        if re.match(found_word_pattern, answer):
            return capitalize_by_question(answer, question)
    return None
