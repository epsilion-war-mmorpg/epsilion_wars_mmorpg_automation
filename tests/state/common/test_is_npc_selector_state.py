from unittest.mock import AsyncMock, Mock

import pytest

from epsilion_wars_mmorpg_automation.game.state.common import is_npc_selector

town_message = """В городе ты можешь найти местных жителей, 
у которых можно купить различную экипировку и снаряжение. 
Также, ты можешь помочь им с решением различных вопросов и задач. 
Они в долгу не останутся.
К кому ты хочешь зайти в гости?"""


def test_is_npc_selector_buttons_not_found():
    event_mock = Mock()
    event_mock.message.message = town_message
    event_mock.message.buttons = []

    result = is_npc_selector(event_mock)

    assert result is False


@pytest.mark.parametrize('payload, expected', [
    (town_message, True),
    ('random message', False),
])
def test_is_npc_selector_happy_path(payload: str, expected: bool):
    button = AsyncMock()
    button.text = 'NPC name'
    button_return = AsyncMock()
    button_return.text = 'Назад'
    event_mock = Mock()
    event_mock.message.message = payload
    event_mock.message.buttons = [[button, button_return]]

    result = is_npc_selector(event_mock)

    assert result is expected
