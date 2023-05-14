"""Combo-bites selector startegies."""
import logging
import random

from telethon import events, types

from epsilion_wars_mmorpg_automation import shared_state
from epsilion_wars_mmorpg_automation.game import parsers
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
    all_options = get_buttons_flat(event)
    current_turn_number = parsers.get_turn_number(event.message.message)
    logging.info('Tuned combo strategy call: turn #{0}, {1}'.format(
        current_turn_number,
        shared_state.COMBO_TURN_LOCKS,
    ))

    if not current_turn_number:
        logging.warning('skip because turn number not found')
        # skip
        return all_options[-2]

    for option in all_options[:-2]:
        locked_turns_count = _get_combo_turn_lock(option.text)
        previous_call_turn = shared_state.COMBO_TURN_LOCKS.get(option.text)
        if not locked_turns_count:
            # not locked option
            shared_state.COMBO_TURN_LOCKS[option.text] = current_turn_number
            return option

        if not previous_call_turn:
            # its first time call og it combo option
            shared_state.COMBO_TURN_LOCKS[option.text] = current_turn_number
            return option

        if current_turn_number >= (previous_call_turn + locked_turns_count):
            # unlocked option
            shared_state.COMBO_TURN_LOCKS[option.text] = current_turn_number
            return option

    # skip
    return all_options[-2]


def _get_combo_turn_lock(combo_name: str) -> int:
    return app_settings.combo_lock_config.get(combo_name, 0)
