"""Grinding event handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import actions, notifications
from epsilion_wars_mmorpg_automation.captcha import resolvers
from epsilion_wars_mmorpg_automation.grind.loop import exit_request
from epsilion_wars_mmorpg_automation.parsers import parsers
from epsilion_wars_mmorpg_automation.settings import app_settings


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
    if app_settings.notifications_enabled:
        await notifications.send_desktop_notify(
            message='battle start\n"{0}"'.format(event.message.message),
        )
    # force recall battle start message
    await actions.ping(event)


async def battle_end_handler(event: events.NewMessage.Event) -> None:
    """Complete win/fail battle."""
    if event.message.button_count:
        await actions.complete_battle(event)

    if app_settings.notifications_enabled:
        await notifications.send_desktop_notify(
            message='battle end\n"{0}"'.format(event.message.message),
        )


async def skip_turn_handler(event: events.NewMessage.Event) -> None:
    """Just skip event."""
    logging.debug('skip event')


async def captcha_fire_handler(event: events.NewMessage.Event) -> None:
    """Try to solve captcha."""
    logging.warning('captcha event shot!')

    if app_settings.notifications_enabled:
        notify_message = parsers.strip_message(event.message.message)
        await notifications.send_desktop_notify(
            message=f'captcha fire!\n"{notify_message}"',
        )

    if app_settings.captcha_solver_enabled:
        captcha_answer = resolvers.try_resolve(event)
        logging.info(f'captcha answer {captcha_answer}')

        if captcha_answer.answer:
            await actions.captcha_answer(event, captcha_answer.answer)
        else:
            await notifications.send_desktop_notify('captcha not solved!')

    elif app_settings.stop_if_captcha_fire:
        exit_request()


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Stop grinding when equip broken."""
    logging.info('equip broken event')
    if app_settings.notifications_enabled:
        notify_message = parsers.strip_message(event.message.message)
        await notifications.send_desktop_notify(
            message=f'equip is broken!\n"{notify_message}"',
        )

    if app_settings.stop_if_equip_broken:
        exit_request()
