import pytest


@pytest.fixture
def mocked_client_message_send(mocker):
    yield mocker.patch('app.actions.client.send_message')
