"""anti-captcha.com service provider for resolve image-to-text captcha."""

import httpx

from epsilion_wars_mmorpg_automation.settings import app_settings


class AntiCaptchaError(RuntimeError):
    """Custom anti-captcha provider error."""

    pass


class AntiCaptchaClient:
    """anti-captcha.com client."""

    _api_host: str = 'https://api.anti-captcha.com'
    _api_key: str
    _timeout: int

    def __init__(self, apikey: str, timeout: int) -> None:
        """Set up api credentials."""
        self._api_key = apikey
        self._timeout = timeout

    async def create_task(self, image_base64: str) -> dict:
        """
        Create task.

        https://anti-captcha.com/ru/apidoc/task-types/ImageToTextTask
        """
        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url=f'{self._api_host}/createTask',
                    timeout=app_settings.anti_captcha_com_timeout,
                    json={
                        'clientKey': self._api_key,
                        'task': {
                            'type': 'ImageToTextTask',
                            'body': image_base64,
                            'phrase': False,
                            'case': False,
                            'numeric': 1,
                            'math': False,
                            'minLength': 1,
                            'maxLength': 6,
                        },
                    },
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise AntiCaptchaError('network error') from fetch_exc

        task_data = response.json()
        error = task_data.get('errorCode')
        if error:
            raise AntiCaptchaError(error)

        return task_data

    async def get_task(self, task_id: int) -> dict:
        """
        Get task.

        https://anti-captcha.com/ru/apidoc/methods/getTaskResult
        """
        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url=f'{self._api_host}/getTaskResult',
                    timeout=app_settings.anti_captcha_com_timeout,
                    json={
                        'clientKey': self._api_key,
                        'taskId': task_id,
                    },
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise AntiCaptchaError('network error') from fetch_exc

        task_data = response.json()
        error = task_data.get('errorCode')
        if error:
            raise AntiCaptchaError(error)

        return task_data


client = AntiCaptchaClient(
    apikey=app_settings.anti_captcha_com_apikey,
    timeout=app_settings.anti_captcha_com_timeout,
)


async def resolve_image_to_number(image_source: str) -> str | None:
    """Create anti-captcha task and wait for answer."""
    # todo impl
    # todo test
    created_task_response = await client.create_task(
        image_base64=image_source,
    )
    # todo wait solve
    # todo max tries
    # todo throttling

    return '1234'
