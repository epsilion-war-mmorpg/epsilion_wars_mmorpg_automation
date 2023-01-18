from epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider import AntiCaptchaError, resolve_image_to_number
from tests.captcha.anti_captcha.conftest import real_captcha_image_base64


async def test_resolve_image_to_number_happy_path(mocker):
    create_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.create_task',
        return_value={
            'taskId': 1234,
            'errorId': 0,
        },
    )
    get_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.get_task',
        return_value={
            'status': 'ready',
            'solution': {'text': '4567'},
        },
    )

    result = await resolve_image_to_number(real_captcha_image_base64)

    assert create_task_mock.call_count == 1
    assert get_task_mock.call_count == 1
    assert result == '4567'


async def test_resolve_image_to_number_create_task_exception(mocker):
    create_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.create_task',
        side_effect=AntiCaptchaError('CREATE TASK ERROR'),
    )
    get_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.get_task',
        return_value={
            'status': 'ready',
            'solution': {'text': '4567'},
        },
    )

    result = await resolve_image_to_number(real_captcha_image_base64)

    assert create_task_mock.call_count == 3
    assert get_task_mock.call_count == 0
    assert result is None


async def test_resolve_image_to_number_task_not_ready(mocker):
    create_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.create_task',
        return_value={
            'taskId': 1234,
            'errorId': 0,
        },
    )
    get_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.get_task',
        return_value={'status': 'processing'},
    )

    result = await resolve_image_to_number(real_captcha_image_base64)

    assert create_task_mock.call_count == 1
    assert get_task_mock.call_count == 8
    assert result is None


async def test_resolve_image_to_number_get_task_exception(mocker):
    create_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.create_task',
        return_value={
            'taskId': 1234,
            'errorId': 0,
        },
    )
    get_task_mock = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider.client.get_task',
        side_effect=AntiCaptchaError('GET TASK ERROR'),
    )

    result = await resolve_image_to_number(real_captcha_image_base64)

    assert create_task_mock.call_count == 1
    assert get_task_mock.call_count == 8
    assert result is None
