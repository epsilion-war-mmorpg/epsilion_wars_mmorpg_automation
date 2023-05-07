from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.game.state.common import is_npc_selector

success_map_message = """В городе ты можешь найти местных жителей, у которых можно купить различную экипировку и снаряжение. Также, ты можешь помочь им с решением различных вопросов и задач. Они в долгу не останутся. 

К кому ты хочешь зайти в гости?"""


def test_is_npc_selector():
    button_mock = Mock()
    button_mock.text = 'Любая кнопка'
    event_mock = Mock()
    event_mock.message.message = success_map_message
    event_mock.message.buttons = [[button_mock]]

    result = is_npc_selector(event_mock)

    assert result is True
