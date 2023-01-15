"""Game-specific captcha resolver."""
from epsilion_wars_mmorpg_automation.captcha.utils import capitalize_by_question

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
            return capitalize_by_question(answer, question)
    return None
