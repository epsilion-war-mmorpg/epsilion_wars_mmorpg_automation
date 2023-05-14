"""Grinding handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import notifications, shared_state, stats
from epsilion_wars_mmorpg_automation.game import action, parsers
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.trainer import loop


async def grinding_handler(event: events.NewMessage.Event) -> None:
    """Start grinding or heal myself."""
    hp_level_percent = parsers.get_hp_level(
        message_content=event.message.message,
    )
    logging.info('current HP level is %d%%', hp_level_percent)

    if hp_level_percent >= app_settings.minimum_hp_level_for_grinding:
        await action.grinding_actions.search_enemy(event)

    elif app_settings.auto_healing_enabled:
        await action.grinding_actions.healing(event)


async def battle_start_handler(event: events.NewMessage.Event) -> None:
    """Notify about battle started."""
    # force recall battle start message
    shared_state.COMBO_TURN_LOCKS = {}
    await action.common_actions.ping(event)


async def battle_end_handler(event: events.NewMessage.Event) -> None:
    """Complete win/fail battle."""
    if event.message.button_count:
        await action.grinding_actions.complete_battle(event)

    stats.collector.inc_value('battles')
    experience_inc = parsers.get_experience_gain(event.message.message)
    if experience_inc:
        stats.collector.inc_value('experience', experience_inc)

    await notifications.send_desktop_notify(
        message=event.message.message,
    )


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Stop grinding when equip broken."""
    logging.info('equip broken event')

    notify_message = parsers.strip_message(event.message.message)
    await notifications.send_desktop_notify(
        message=notify_message,
        is_urgent=True,
    )

    if app_settings.stop_if_equip_broken:
        loop.exit_request()
