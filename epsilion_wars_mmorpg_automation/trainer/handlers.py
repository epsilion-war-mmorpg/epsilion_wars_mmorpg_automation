"""Grinding event handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import notifications, stats
from epsilion_wars_mmorpg_automation.captcha import resolvers
from epsilion_wars_mmorpg_automation.game import actions, parsers
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.trainer.loop import exit_request


async def hunting_handler(event: events.NewMessage.Event) -> None:
    """Start hunting or heal myself."""
    hp_level_percent = parsers.get_hp_level(
        message_content=event.message.message,
    )
    logging.info('current HP level is %d%%', hp_level_percent)

    if hp_level_percent >= app_settings.minimum_hp_level_for_grinding:
        await actions.search_enemy(event)

    elif app_settings.auto_healing_enabled:
        await actions.healing(event)


async def battle_start_handler(event: events.NewMessage.Event) -> None:
    """Notify about battle started."""
    # force recall battle start message
    await actions.ping(event)


async def battle_end_handler(event: events.NewMessage.Event) -> None:
    """Complete win/fail battle."""
    if event.message.button_count:
        await actions.complete_battle(event)

    stats.collector.inc_value('battles')
    experience_inc = parsers.get_experience_gain(event.message.message)
    if experience_inc:
        stats.collector.inc_value('experience', experience_inc)

    await notifications.send_desktop_notify(
        message=event.message.message,
    )


async def skip_turn_handler(event: events.NewMessage.Event) -> None:
    """Just skip event."""
    logging.debug('skip event')


async def captcha_fire_handler(event: events.NewMessage.Event) -> None:
    """Try to solve captcha."""
    logging.warning('captcha event shot!')

    stats.collector.inc_value('captcha-s')
    notify_message = parsers.strip_message(event.message.message)
    await notifications.send_desktop_notify(
        message=notify_message,
        is_urgent=True,
    )

    if app_settings.captcha_solver_enabled:
        captcha_answer = await resolvers.try_resolve(event)
        logging.info(f'captcha answer {captcha_answer}')

        if captcha_answer.answer:
            await notifications.send_desktop_notify(f'captcha answer found:\n"{captcha_answer.answer}"')
            await actions.captcha_answer(event, captcha_answer.answer)
        else:
            await notifications.send_desktop_notify('captcha not solved!', is_urgent=True)

    elif app_settings.stop_if_captcha_fire:
        exit_request()


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Stop grinding when equip broken."""
    logging.info('equip broken event')

    notify_message = parsers.strip_message(event.message.message)
    await notifications.send_desktop_notify(
        message=notify_message,
        is_urgent=True,
    )

    if app_settings.stop_if_equip_broken:
        exit_request()
