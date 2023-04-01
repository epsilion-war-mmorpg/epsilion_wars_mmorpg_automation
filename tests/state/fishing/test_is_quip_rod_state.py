from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.fishing import is_equip_rod_state


def test_is_equip_rod_state_happy_path():
    button_rod = AsyncMock()
    button_rod.text = '✅ Надеть'

    event_mock = Mock()
    event_mock.message.message = '🔪 удочка ученика [i] :  позволяет участвовать в рыбалке  ❇️ тип предмета'
    event_mock.message.buttons = [[button_rod]]

    result = is_equip_rod_state(event_mock)

    assert result is True
