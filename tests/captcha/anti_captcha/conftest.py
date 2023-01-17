import pytest

from epsilion_wars_mmorpg_automation.captcha.anti_captcha_provider import AntiCaptchaClient
from epsilion_wars_mmorpg_automation.settings import app_settings


def anti_captcha_configured() -> bool:
    return len(app_settings.anti_captcha_com_apikey) > 0
