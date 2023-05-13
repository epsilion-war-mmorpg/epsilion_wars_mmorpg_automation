"""Combo-bites selector startegies."""
import random

from telethon import events, types

from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings


def simple_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return the first punch always, default strategy."""
    combo_options = get_buttons_flat(event)[:-2]
    return combo_options[0]


def random_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return a random one available."""
    combo_options = get_buttons_flat(event)[:-2]
    return random.choice(combo_options)


def random_or_skip_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return a random one available or skip."""
    all_options = get_buttons_flat(event)
    if random.randint(0, 100) <= app_settings.skip_combo_chance:
        return all_options[-2]
    return random.choice(all_options[:-2])


def disabled_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return skip button always."""
    all_options = get_buttons_flat(event)
    return all_options[-2]


def tuned_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return combo bite based on its previous use."""
    # todo
    all_options = get_buttons_flat(event)
    return all_options[-2]
