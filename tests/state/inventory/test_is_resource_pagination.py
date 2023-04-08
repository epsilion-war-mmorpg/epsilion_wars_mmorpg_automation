from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.inventory import is_resource_pagination


async def test_is_resource_pagination_happy_path():
    button1 = AsyncMock()
    button1.text = '➡'
    button2 = AsyncMock()
    button2.text = '♻️ К ресурсам'

    event_mock = Mock()
    event_mock.message.buttons = [[button1, button2]]

    result = is_resource_pagination(event_mock)

    assert result is True


async def test_is_resource_pagination_without_pages():
    button = AsyncMock()
    button.text = '♻️ К ресурсам'

    event_mock = Mock()
    event_mock.message.buttons = [[button]]

    result = is_resource_pagination(event_mock)

    assert result is True
