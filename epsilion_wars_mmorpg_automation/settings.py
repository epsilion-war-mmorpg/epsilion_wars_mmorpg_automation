"""Application settings."""
import os

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Application settings class."""

    telegram_api_id: int = 123456
    telegram_api_hash: str = 'u_api_hash_here'
    debug: bool = Field(default=False, description='Logging level')
    game_username: str = 'EpsilionWarBot'
    minimum_hp_level_for_grinding: int = Field(default=70, ge=1, le=100)
    ping_message: str = '/me'
    message_log_limit: int = 100


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
