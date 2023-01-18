import pytest

from epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider import AntiCaptchaClient, AntiCaptchaError, client
from tests.captcha.anti_captcha.conftest import anti_captcha_configured, real_captcha_image_base64


@pytest.mark.parametrize('apikey', ['', 'sdsdsdsd'])
async def test_client_init(apikey: str):
    result = AntiCaptchaClient(apikey, 15)

    assert result


@pytest.mark.skipif(
    not anti_captcha_configured(), reason="requires configured anti_captcha_com_apikey in settings"
)
async def test_client_get_task_not_found():
    with pytest.raises(AntiCaptchaError, match='ERROR_NO_SUCH_CAPCHA_ID'):
        await client.get_task(0)


@pytest.mark.skipif(
    not anti_captcha_configured(), reason="requires configured anti_captcha_com_apikey in settings"
)
@pytest.mark.skip(reason="Disable by finance reason - every solved captcha cut balance =)")
async def test_client_get_task_success():
    captcha_id = await test_client_create_task_success()

    result = await client.get_task(captcha_id)

    assert result['status'] in {'ready', 'processing'}
    if result['status'] == 'ready':
        assert result['solution']['text'] == '4594'


@pytest.mark.skipif(
    not anti_captcha_configured(), reason="requires configured anti_captcha_com_apikey in settings"
)
async def test_client_create_task_empty_image(payload: str, expected_error: str):
    with pytest.raises(AntiCaptchaError, match='ERROR_ZERO_CAPTCHA_FILESIZE'):
        await client.create_task('sdsdsdsd')


@pytest.mark.skipif(
    not anti_captcha_configured(), reason="requires configured anti_captcha_com_apikey in settings"
)
async def test_client_create_task_empty_image():
    with pytest.raises(AntiCaptchaError, match='ERROR_IMAGE_TYPE_NOT_SUPPORTED'):
        await client.create_task(f'invalid_base64{real_captcha_image_base64}')


@pytest.mark.skipif(
    not anti_captcha_configured(), reason="requires configured anti_captcha_com_apikey in settings"
)
@pytest.mark.skip(reason="Disable by finance reason - every solved captcha cut balance =)")
async def test_client_create_task_success() -> int:
    result = await client.create_task(real_captcha_image_base64)

    assert result['taskId']
    assert result['errorId'] == 0

    return result['taskId']
