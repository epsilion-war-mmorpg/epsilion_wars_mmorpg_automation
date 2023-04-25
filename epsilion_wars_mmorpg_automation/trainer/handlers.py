"""Grinding event handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import notifications, shared_state, stats
from epsilion_wars_mmorpg_automation.captcha import resolvers
from epsilion_wars_mmorpg_automation.game import action, parsers, state
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
            await action.common_actions.captcha_answer(event, captcha_answer.answer)
        else:
            await notifications.send_desktop_notify('captcha not solved!', is_urgent=True)

    elif app_settings.stop_if_captcha_fire:
        loop.exit_request()


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


async def fishing_start(event: events.NewMessage.Event) -> None:
    """Start fishing."""
    logging.info('start fishing event')
    response = await action.fishing_actions.select_fishing_type(event)
    if response:
        logging.info(f'{response.message=}')
        if state.fishing_states.is_rod_equip_needed(response.message):
            await action.common_actions.show_equip(event)


async def fishing_end(event: events.NewMessage.Event) -> None:
    """Restart fishing after end."""
    logging.info('end fishing event')
    await action.fishing_actions.complete_fishing(event)
    await action.fishing_actions.start_fishing(event.chat_id)


async def collect_resource_counters(event: events.NewMessage.Event) -> None:
    """Collect resource counters to shared state."""
    logging.info('collect resource counters')

    resource_counters = parsers.get_resource_counters(event.message.message)
    logging.info('collect counters {0}'.format(resource_counters))
    shared_state.RESOURCE_COUNTERS.update(resource_counters)

    if state.inventory_states.has_show_next_page_button(event):
        await action.inventory_actions.show_next_page(event)
    else:
        logging.info('next page not found - force exit')
        loop.exit_request()
