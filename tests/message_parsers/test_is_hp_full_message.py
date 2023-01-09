import pytest

from app.message_parsers import is_hp_full_message


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('💖 Ваше здоровье полностью восстановлено', True),
])
def test_is_hp_full_message(payload: str, expected: bool):
    result = is_hp_full_message(payload)

    assert result is expected
