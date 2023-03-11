from unittest.mock import Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.common import is_equip_broken_message


@pytest.mark.parametrize('payload,expected', [
    ('не то сообщение', False),
    ('⚠️ Экипировка Потертая тарга - снята из-за поломки', True),
])
def test_is_equip_broken_message(payload: str, expected: bool):
    event_mock = Mock()
    event_mock.message.message = payload

    result = is_equip_broken_message(event_mock)

    assert result is expected
