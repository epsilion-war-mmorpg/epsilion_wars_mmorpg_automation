"""Application settings."""
import os

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Application settings class."""

    debug: bool = Field(False, description='Logging level')
    telegram_api_id: int
    telegram_api_hash: str
    game_username: str = 'EpsilionWarBot'
    minimum_hp_level_for_grinding: int = 70
    ping_message: str = '/me'


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
