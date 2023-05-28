"""Application settings."""
import os
from typing import Literal

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Application settings class."""

    # required customer settings
    telegram_api_id: int = 123456
    telegram_api_hash: str = 'u_api_hash_here'

    # optional customer settings
    minimum_hp_level_for_grinding: int = Field(default=95, ge=1, le=100)
    notifications_enabled: bool = True
    favorites_enabled: bool = True
    auto_healing_enabled: bool = True
    stop_if_equip_broken: bool = True
    stop_if_captcha_fire: bool = False
    captcha_solver_enabled: bool = True

    select_combo_strategy: Literal['simple', 'random', 'random-or-skip', 'disabled', 'tuned'] = 'simple'
    skip_combo_chance: int = Field(default=30, description='Chance to skip combo bite if `random-or-skip` strategy selected')

    skip_random_vendor: bool = True
    skip_random_vendor_stop_words: str = 'Свиток Кселеса,Безопасный свиток заточки [IV]'
    use_backup_game_bot: bool = False
    equip_farming_number: int = 1
    equip_travel_number: int = 2
    repair_locations_path: str = ''
    custom_channel_for_inventory: str = ''

    # advanced customer settings
    anti_captcha_com_apikey: str = Field(default='', description='see https://anti-captcha.com for more information')
    anti_captcha_com_timeout: int = 15
    anti_captcha_com_create_task_tries: int = 3
    anti_captcha_com_create_task_throttling: int = 15
    anti_captcha_com_get_task_tries: int = 20
    anti_captcha_com_get_task_throttling: int = 5
    healing_timeout: int = Field(
        default=20,
        description='Минимальное количество секунд между двумя использованиями зелий восстановления здоровья.',
    )

    # developer section
    slow_mode: bool = Field(default=False, description='Used for fresh telegram accounts.')
    ping_commands: str = ',.-+=/056789'
    game_username: str = 'EpsilionWarBot'
    game_username_backup: str = 'EpsilionRBRbot'
    tlg_client_retries: int = 30
    tlg_client_retry_delay: int = 15
    trainer_name: str = 'Epsilion Trainer'
    trainer_public_link: str = 'https://github.com/esemi/epsilion_wars_mmorpg_automation/'
    debug: bool = Field(default=False)
    message_log_limit: int = 100
    hp_level_for_low_heal_pot: int = Field(default=75, ge=1, le=100)
    hp_level_for_mid_heal_pot: int = Field(default=50, ge=1, le=100)
    rod_minimal_hp_level_for_fishing: int = Field(default=3, ge=1)
    bow_minimal_hp_level_for_hunting: int = Field(default=8, ge=1)
    equip_minimal_hp_level_for_repairing: int = Field(default=1, ge=1)
    character_middle_level_threshold: int = 10
    character_high_level_threshold: int = 20
    character_top_level_threshold: int = 30
    wait_loop_iteration_seconds: int = 3
    show_stats_every_seconds: int = 30 * 60
    check_rewards_every_seconds: int = 4 * 60 * 60
    check_fishing_every_seconds_min: int = int(0.95 * 60 * 60)
    check_fishing_every_seconds_max: int = int(2.01 * 60 * 60)
    check_hunting_every_seconds_min: int = int(2.95 * 60 * 60)
    check_hunting_every_seconds_max: int = int(4.01 * 60 * 60)
    desktop_notification_timeout: int = 10
    repairman_locations: list[str] = [
        'Кавелла',
        'Дранг',
        'Аквелия',
        'Цирта',
        'Древние руины',
        'Северный порт',
        'Лонгйир',
        'Карбарак',
        'Оазис',
        # fixme put T4 locations here
    ]
    repairman_names: set[str] = {
        '⚒ Кузнец Эрик',
        '⚒ Кузнец Грыл',
        '⚒ Кузнец Гейл',
        '⚒ Кузнец Хэнк',
        '⚒ Кузнец Аакмаан',
        '⚒ Кузнец Флэт',
        '⚒ Мастер брони Эгерь',
        '⚒ Кузнец Карбо',
        '⚒ Кузнец Оазис',
        # fixme put T4 repairman names here
    }
    combo_lock_config: dict[str, int] = {
        'Атакующая волна I(🗡1🥊1)': 3,
        'Обряд оков I(🥊1🌬1)': 2,
    }
    combo_heal_hp: dict[str, int] = {
        'Жизненная сила I(🗡1🥊1)': 450,
    }


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)

game_bot_name = app_settings.game_username_backup if app_settings.use_backup_game_bot else app_settings.game_username
