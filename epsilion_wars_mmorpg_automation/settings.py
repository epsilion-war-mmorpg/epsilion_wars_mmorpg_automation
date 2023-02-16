"""Application settings."""
import os

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Application settings class."""

    # required customer settings
    telegram_api_id: int = 123456
    telegram_api_hash: str = 'u_api_hash_here'

    # optional customer settings
    minimum_hp_level_for_grinding: int = Field(default=93, ge=1, le=100)
    notifications_enabled: bool = True
    auto_healing_enabled: bool = True
    stop_if_equip_broken: bool = True
    stop_if_captcha_fire: bool = False
    captcha_solver_enabled: bool = True

    # advanced customer settings
    anti_captcha_com_apikey: str = Field(default='', description='see https://anti-captcha.com for more information')
    anti_captcha_com_timeout: int = 15
    anti_captcha_com_create_task_tries: int = 3
    anti_captcha_com_create_task_throttling: int = 15
    anti_captcha_com_get_task_tries: int = 20
    anti_captcha_com_get_task_throttling: int = 5

    # developer section
    game_username: str = 'EpsilionWarBot'
    tlg_client_retries: int = 30
    tlg_client_retry_delay: int = 15
    trainer_name: str = 'Epsilion Trainer'
    debug: bool = Field(default=False, description='Logging level')
    message_log_limit: int = 100
    hp_level_for_low_heal_pot: int = Field(default=75, ge=1, le=100)
    hp_level_for_mid_heal_pot: int = Field(default=50, ge=1, le=100)
    character_top_level_threshold: int = 30
    character_high_level_threshold: int = 20
    character_middle_level_threshold: int = 10
    wait_loop_iteration_seconds: int = 3
    show_stats_every_seconds: int = 30 * 60
    desktop_notification_timeout: int = 10


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
