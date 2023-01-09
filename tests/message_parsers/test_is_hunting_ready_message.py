import pytest

from app.message_parsers import is_hunting_ready_message


@pytest.mark.parametrize('payload,expected', [
    ('ololo', False),
    ('❕ Информация: /hunt_info\nВ локации можно встретить врагов. Кто же будет следующим?', True),
])
def test_is_hunting_ready_message(payload: str, expected: bool):
    result = is_hunting_ready_message(payload)

    assert result is expected
