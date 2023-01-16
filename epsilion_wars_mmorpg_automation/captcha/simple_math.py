"""Resolver for simple math operations captcha."""

import math
import operator
import re

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import convert_number_words

_math_patterns = [
    re.compile(r'(\d+)(.+?)(\d+)-нaпишитеответчислом'),
    re.compile(r'(.+?)(\d+)-нaпишитеответчислом'),
]


def simple_math(message: str) -> str | None:
    """Resolve simple math operations captcha."""
    try:
        question = message.split('\n')[1].lower()
    except IndexError:
        return None

    operator_str, operands = _get_math_operation(
        question=convert_number_words(question.replace(' ', '')),
    )
    if not operator_str:
        return None

    operation = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        'x': operator.mul,
        'х': operator.mul,
        '/': operator.truediv,
        'плюс': operator.add,
        'минус': operator.sub,
        'умножитьнa': operator.mul,
        'умножнa': operator.mul,
        'умннa': operator.mul,
        'делитьнa': operator.truediv,
        'делинa': operator.truediv,
        'делнa': operator.truediv,
        'кореньиз': math.sqrt,
    }.get(operator_str)

    if not operation:
        return None

    return str(int(operation(*operands)))  # type: ignore


def _get_math_operation(question: str) -> tuple[str | None, list[int]]:
    operator_str = None
    operands = []
    for pattern in _math_patterns:
        found = pattern.search(question)
        operands = _get_operands(found)
        operator_str = _get_operation_name(found)
        if operator_str:
            break

    if operator_str:
        return operator_str.replace('.', ''), operands
    return None, []


def _get_operands(match: re.Match | None) -> list[int]:
    if not match:
        return []

    operands = []
    if len(match.groups()) == 3:
        operands = [match.group(1), match.group(3)]

    elif len(match.groups()) == 2:
        operands = [match.group(2)]

    try:
        return [int(op_value) for op_value in operands]
    except ValueError:
        return []


def _get_operation_name(match: re.Match | None) -> str | None:
    if not match:
        return None

    if len(match.groups()) == 3:
        return match.group(2)

    if len(match.groups()) == 2:
        return match.group(1)

    return None
