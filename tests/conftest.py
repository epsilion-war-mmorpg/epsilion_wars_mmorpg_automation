import asyncio
import os

import pytest

os.environ.setdefault('EPSA_DISABLE_DOTENV', '1')
os.environ.pop('DEBUG', None)

from epsilion_wars_mmorpg_automation.settings import app_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def combo_priority_strategy_overloaded():
    saved_value = app_settings.combo_priority
    app_settings.combo_priority = {
        'Внутренняя сила (2🗡; 3🛡)': 2,
        'По наитию (3 🥊)': 1,
    }

    yield

    app_settings.combo_priority = saved_value
