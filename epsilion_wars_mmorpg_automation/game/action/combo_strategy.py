"""Combo-bites selector startegies."""
import logging
import random

from telethon import events, types

from epsilion_wars_mmorpg_automation import exceptions, shared_state
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


def priority_strategy(event: events.NewMessage.Event) -> types.TypeKeyboardButton:
    """Return a combo bite by priority."""
    options_by_priority: list[tuple[types.TypeKeyboardButton, int]] = [
        (combo, app_settings.combo_priority.get(combo.text, 100))
        for combo in get_buttons_flat(event)[:-2]
    ]
    options_by_priority.sort(
        key=lambda button: button[1],
    )
    return options_by_priority[0][0]


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
        return all_options[-2]

    if heal_option := _try_heal_first(all_options, current_turn_number, event.message.message):
        logging.info('heal first {0}'.format(heal_option.text))
        return heal_option

    if bite_option := _try_use_bite_combo(all_options, current_turn_number):
        logging.info('selected bite {0}'.format(bite_option.text))
        return bite_option

    logging.info('skip combo')
    return all_options[-2]


def _get_combo_turn_lock(combo_name: str) -> int:
    return app_settings.combo_lock_config.get(combo_name, 0)


def _get_combo_heal_hp_level(combo_name: str) -> int:
    return app_settings.combo_heal_hp.get(combo_name, 0)


def _try_heal_first(
    all_options: list[types.TypeKeyboardButton],
    current_turn_number: int,
    message: str,
) -> types.TypeKeyboardButton | None:
    try:
        character_hp_current, character_hp_max = parsers.get_character_hp(message)
    except exceptions.InvalidMessageError:
        return None

    character_hp_diff = character_hp_max - character_hp_current
    logging.info('character HP {0}/{1}'.format(
        character_hp_current,
        character_hp_max,
    ))

    for option in all_options[:-2]:
        combo_heal_power = _get_combo_heal_hp_level(option.text)
        if combo_heal_power and combo_heal_power <= character_hp_diff:
            logging.info('select heal combo option "{2}"; HP {0} <= {1}'.format(
                combo_heal_power,
                character_hp_diff,
                option.text,
            ))
            shared_state.COMBO_TURN_LOCKS[option.text] = current_turn_number
            return option

    return None


def _try_use_bite_combo(
    all_options: list[types.TypeKeyboardButton],
    current_turn_number: int,
) -> types.TypeKeyboardButton | None:
    for option in all_options[:-2]:
        if _get_combo_heal_hp_level(option.text):
            # ignore heal combos
            continue

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
    return None
