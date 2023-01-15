"""Captcha resolvers utils."""


def capitalize_by_question(answer: str, message: str) -> str:
    """Capitalize answer by question request."""
    if 'ответсмаленькойбуквы' in message:
        return answer.lower()
    if 'ответсбольшойбуквы' in message:
        return answer.capitalize()
    return answer
