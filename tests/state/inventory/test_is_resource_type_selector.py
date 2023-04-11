from unittest.mock import AsyncMock, Mock

from epsilion_wars_mmorpg_automation.game.state.inventory import is_resource_type_selector


async def test_is_resource_type_selector_happy_path():
    button = AsyncMock()
    button.text = '⚒ Крафтовые [29]'

    event_mock = Mock()
    event_mock.message.message = '♻️ Ресурсы\n\n❓ Ресурсы обычно используются для крафта, но могут быть другие применения'
    event_mock.message.buttons = [[button]]

    result = is_resource_type_selector(event_mock)

    assert result is True


async def test_is_resource_type_selector_not_found():
    event_mock = Mock()
    event_mock.message.message = '♻️ Ресурсы\n\n❓ Ресурсы обычно используются для крафта, но могут быть другие применения\n\n❗️ Ресурсов в инвентаре пока нет, убивайте монстров в локациях для их получения.'
    event_mock.message.buttons = []

    result = is_resource_type_selector(event_mock)

    assert result is False
