"""Common handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation import notifications, shared_state, stats
from epsilion_wars_mmorpg_automation.captcha import resolvers
from epsilion_wars_mmorpg_automation.game import action, parsers, state
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.trainer import loop


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
