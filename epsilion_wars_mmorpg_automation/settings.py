"""Application settings."""
import os
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

APP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)


class AppSettings(BaseSettings):
    """Application settings class."""

    # required customer settings
    telegram_api_id: int = 123456
    telegram_api_hash: str = 'u_api_hash_here'

    # optional customer settings
    minimum_hp_level_for_grinding: int = Field(default=95, ge=1, le=100)
    grinding_time_limit_minutes: int | None = Field(default=None)
    notifications_enabled: bool = False
    favorites_enabled: bool = True
    auto_healing_enabled: bool = True
    self_manager_enabled: bool = True
    stop_if_equip_broken: bool = True
    stop_if_captcha_fire: bool = False
    check_daily_rewards: bool = True
    captcha_solver_enabled: bool = True

    select_combo_strategy: Literal['simple', 'random', 'random-or-skip', 'disabled', 'tuned', 'priority'] = 'simple'
    skip_combo_chance: int = Field(
        default=30,
        description='Chance to skip combo bite if `random-or-skip` strategy selected',
    )

    skip_random_vendor: bool = True
    skip_random_vendor_stop_words: str = ''
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
    fast_mode: bool = Field(default=False)
    slow_mode: bool = Field(default=False, description='Used for fresh telegram accounts.')
    ping_commands: str = ',.-+=/0'
    game_username: str = 'EpsilionWarBot'
    game_username_backup: str = 'EpsilionRBRbot'
    tlg_client_retries: int = 30
    tlg_client_retry_delay: int = 15
    trainer_name: str = 'Epsilion Trainer'
    trainer_public_link: str = 'https://teletype.in/@esemiko/epsilion-trainer'
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
    check_fishing_every_seconds_min: int = int(2.95 * 60 * 60)
    check_fishing_every_seconds_max: int = int(5.01 * 60 * 60)
    check_hunting_every_seconds_min: int = int(5.95 * 60 * 60)
    check_hunting_every_seconds_max: int = int(9.01 * 60 * 60)
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
        'Поселение Троглодитов',
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
        'Кузнец Горд',
    }
    combo_lock_config: dict[str, int] = {
        # Inquisitor
        'Обряд оков I(🥊1🌬1)': 2,
        'Атакующая волна I(🗡1🥊1)': 3,
        'Обряд ярости I(🗡1🌬2)': 3,
        'Обряд вдохновения I(🗡1🌬2)': 3,
        'Обряд защиты I(🛡1🌬2)': 3,
        'Самозащита I(🗡1🛡1)': 3,
        'Длань восстановления I(🗡1🛡1🥊1)': 4,
        'Благословение ветра I(🗡1🛡1🌬1)': 3,
        # Gladiator
        'Порез ног I(🛡1🌬2)': 2,
        'Мастер дуэлей I(🗡1🛡1🌬2)': 3,
        # Heal
        'Древняя регенерация(1🗡)': 3,
        'Сияние регенерации I(🛡1🌬1)': 3,
        'Немота I(🗡1🛡1🌬1)': 3,
        'Ослабляющие клеймо I(🌬2)': 3,
        # Sentinel
        'Мастерство щита I(🛡3🌬1)': 3,
        'Провокация I(🗡1🛡1)': 3,
        'Стена щитов I(🛡3)': 2,
        'Покровительство I(🗡2)': 3,
        'Гнев I(🛡3)': 3,
        'Броня баланса(🛡4)': 2,
        # Assasin
        'Метка охоты I(🌬1)': 3,
        'Метка жертвы I(🌬2)': 3,
        'Взрывная метка I(🥊1)': 4,
        'Метка молчания I(🛡2)': 3,
        'Сломать оружие I(🛡1🥊1)': 4,
        'Защитная метка I(🛡1🥊2)': 2,
        'Яд змеи I(🗡1🌬1)': 3,
        'Клятва точности I(🥊1🌬1)': 2,
        'Яд скорпиона I(🗡2🥊1)': 4,
        'Кровоточащий удар I(🛡1🥊1)': 3,
        'Обострение чувств I(🥊2)': 3,
        # Hunter"
        'Благословение охоты I(⚡️2)': 3,
        'Сосредоточение I(🌬2)': 3,
        'Удушающая ловушка I(🌬3)': 2,
        'Дымовая бомба I(🗡1⚡️1)': 5,
        'Иллюзия I(🤺2)': 2,
    }
    combo_heal_hp: dict[str, int] = {
        'Жизненная сила I(🗡1🥊1)': 450,
        'Древняя регенерация (1🗡)': 150,
        'Еще одна попытка I(🗡1🛡1🥊1)': 500,
        '🍞 Корка хлеба [II]': 75,
        '🥪 Бутерброд [III]': 200,
        '🥮 Пирог [IV]': 300,
    }
    combo_priority: dict[str, int] = {
        # 'Название приёма целиком': приоритет (чем меньше число - тем выше приоритет)
        'Внутренняя сила (2🗡; 3🛡)': 2,
        'По наитию (3 🥊)': 1,
    }
    use_potions: bool = Field(default=True)
    enabled_potions: set[str] = {
        '/use_reg24',
        '/use_reg7',
        '/use_reg3',
        '/use_meat_eat',
        '/use_fish_eat',
        '/use_acvelia_eat',
        '/use_snack_1',
        '/use_snack_2',
        '/use_snack_3',
        '/use_buff_agi_1_1',
        '/use_buff_agi_2_1',
        '/use_buff_str_1_1',
        '/use_buff_str_2_1',
        '/use_buff_int_1_1',
        '/use_buff_int_2_1',
    }
    use_scrolls: bool = Field(default=True)
    enabled_scrolls: set[str] = {
        '/use_p_luck',
        '/use_luck',
        '/use_prem24',
        '/use_prem3',
        '/use_prem7',
        '/use_p_exp',
        '/use_pgold',
    }


def _get_env_file() -> str | None:
    if os.environ.get('EPSA_DISABLE_DOTENV') == '1':
        return None
    return os.environ.get('EPSA_ENV_FILE') or os.path.join(APP_PATH, '.env')


app_settings = AppSettings(
    _env_file=_get_env_file(),  # type: ignore
)

game_bot_name = app_settings.game_username_backup if app_settings.use_backup_game_bot else app_settings.game_username
