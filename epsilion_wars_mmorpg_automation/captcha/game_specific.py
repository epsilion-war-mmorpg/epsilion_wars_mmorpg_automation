"""Game-specific captcha resolver."""

_question_answer = {
    'столицaэпсилионa': 'Мелидон',
}


def game_specific(message: str) -> str | None:
    """Answers for game-specific questions."""
    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    for question_pattern, answer in _question_answer.items():
        if question_pattern in question:
            return _capitalize_by_question(answer, question)
    return None


def _capitalize_by_question(answer: str, message: str) -> str:
    if 'ответсмаленькойбуквы' in message:
        return answer.lower()
    if 'ответсбольшойбуквы' in message:
        return answer.capitalize()
    return answer
