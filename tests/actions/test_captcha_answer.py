from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.actions import captcha_answer


async def test_captcha_answer_happy_path(mocked_client_message_send):
    event_mock = Mock()
    event_mock.chat_id = 123456

    await captcha_answer(event_mock, 'answer 1234')

    assert mocked_client_message_send.call_count == 1
