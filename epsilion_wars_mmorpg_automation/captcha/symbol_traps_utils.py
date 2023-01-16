"""Captcha resolvers utils for fixing captcha symbol-traps."""


def capitalize_by_question(answer: str, message: str) -> str:
    """Capitalize answer by question request."""
    if 'ответсмаленькойбуквы' in message:
        return answer.lower()
    if 'ответсбольшойбуквы' in message:
        return answer.capitalize()
    return answer


def replace_eng_chars(source: str) -> str:
    """Replace eng chars by ru."""
    mapping = dict(zip('abcekmnopruy', 'аьсектпоргиу'))
    return ''.join([
        mapping.get(char, char)
        for char in source
    ])


def convert_number_words(source: str) -> str:
    """Convert a number from rus word representation to int."""
    mapping = ['один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять']

    output = source
    for index, pattern in enumerate(mapping):
        output = output.replace(pattern, str(index + 1))
    return output
