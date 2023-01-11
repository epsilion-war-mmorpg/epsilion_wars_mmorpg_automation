"""Telegram client."""

from telethon import TelegramClient

from epsilion_wars_mmorpg_automation.settings import app_settings

client = TelegramClient(
    session='.epsilion_automation_session',
    api_id=app_settings.telegram_api_id,
    api_hash=app_settings.telegram_api_hash,
)
