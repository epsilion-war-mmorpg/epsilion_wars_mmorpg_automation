"""anti-captcha.com service provider for resolve image-to-text captcha."""
import asyncio
import logging
from typing import Any

import httpx

from epsilion_wars_mmorpg_automation.settings import app_settings

TASK_READY_STATE = 'ready'


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
            logging.info('request createTask')
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
        logging.info('response createTask {0}'.format(task_data))
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
            logging.info('request getTaskResult')
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
        logging.info('response getTaskResult {0}'.format(task_data))
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
    created_task_response = await _call_create_few_times(
        call_count_limit=app_settings.anti_captcha_com_create_task_tries,
        throttling_time=app_settings.anti_captcha_com_create_task_throttling,
        image_base64=image_source,
    )
    logging.info('AntiCaptchaClient create task response: %s', created_task_response)
    if not created_task_response:
        return None

    task_solution_response = await _call_get_few_times(
        call_count_limit=app_settings.anti_captcha_com_get_task_tries,
        throttling_time=app_settings.anti_captcha_com_get_task_throttling,
        task_id=created_task_response.get('taskId'),
    )
    logging.info('AntiCaptchaClient get task response: %s', task_solution_response)
    if not task_solution_response:
        return None

    return task_solution_response.get('solution', {}).get('text', None)


async def _call_create_few_times(call_count_limit: int, throttling_time: int, **kwargs: Any) -> dict | None:
    try_num = 0

    while try_num < call_count_limit:
        try_num += 1
        try:
            return await client.create_task(**kwargs)
        except AntiCaptchaError as exc:
            logging.warning(f'AntiCaptchaClient error: {exc}')
            await asyncio.sleep(throttling_time)

    return None


async def _call_get_few_times(call_count_limit: int, throttling_time: int, **kwargs: Any) -> dict | None:
    try_num = 0

    while try_num < call_count_limit:
        try_num += 1
        try:
            task_data = await client.get_task(**kwargs)
        except AntiCaptchaError as exc:
            logging.warning(f'AntiCaptchaClient error: {exc}')
            await asyncio.sleep(throttling_time)
            continue

        if task_data.get('status') == TASK_READY_STATE:
            return task_data

    return None
