from unittest.mock import Mock

from epsilion_wars_mmorpg_automation.captcha.image_with_numbers import image_with_numbers


valid_captcha_message = '❓ На пути ты встретил капчу, отправь число с картинки или отправишься в тюрьму. У тебя есть 90 секунд'


async def test_image_with_numbers_happy_path(mocker):
    event_mock = Mock()
    event_mock.message.media = 'media content mocked'
    anticaptcha_mocked = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.image_with_numbers.anti_captcha_provider.resolve_image_to_number',
        return_value='1234',
    )
    base64_getter_mocked = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.image_with_numbers.get_photo_base64',
        return_value='base64/sdsd/sd/sd',
    )

    result = await image_with_numbers(
        message=valid_captcha_message,
        event=event_mock,
    )

    assert base64_getter_mocked.call_count == 1
    assert anticaptcha_mocked.call_count == 1
    assert result == '1234'


async def test_image_with_numbers_have_no_media():
    event_mock = Mock()
    event_mock.message.media = None

    result = await image_with_numbers(
        message=valid_captcha_message,
        event=event_mock,
    )

    assert result is None


async def test_image_with_numbers_skip_by_message():
    event_mock = Mock()
    event_mock.message.media = 'media content mocked'

    result = await image_with_numbers(
        message='сообщение из другой капчи',
        event=event_mock,
    )

    assert result is None


async def test_image_with_numbers_media_not_loaded(mocker):
    event_mock = Mock()
    event_mock.message.media = 'media content mocked'
    base64_getter_mocked = mocker.patch(
        'epsilion_wars_mmorpg_automation.captcha.image_with_numbers.get_photo_base64',
        return_value='',
    )

    result = await image_with_numbers(
        message=valid_captcha_message,
        event=event_mock,
    )

    assert result is None
    assert base64_getter_mocked.call_count == 1
