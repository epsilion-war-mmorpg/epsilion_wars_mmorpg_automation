import pytest


@pytest.fixture
def mocked_client_message_send(mocker):
    yield mocker.patch('epsilion_wars_mmorpg_automation.game.actions.client.send_message')
