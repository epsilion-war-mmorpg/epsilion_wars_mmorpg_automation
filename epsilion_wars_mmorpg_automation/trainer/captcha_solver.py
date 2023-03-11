"""Captcha-solver tool."""
import logging

from telethon import events, types

from epsilion_wars_mmorpg_automation import stats
from epsilion_wars_mmorpg_automation.game.state import common as common_states
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.trainer import event_logging, handlers, loop


async def main() -> None:
    """Captcha-solver runner."""
    local_settings = {
        'notifications_enabled': app_settings.notifications_enabled,
        'captcha_solver_enabled': app_settings.captcha_solver_enabled,
        'anti_captcha_enabled': bool(app_settings.anti_captcha_com_apikey),
    }
    logging.info(f'start captcha-solver ({local_settings=})')

    if not app_settings.captcha_solver_enabled:
        logging.warning('Enable captcha_solver_enabled setting first')
        return

    game_user: types.InputPeerUser = await client.get_input_entity(app_settings.game_username)
    logging.info('game user is %s', game_user)

    client.add_event_handler(
        callback=_message_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    await loop.run_wait_loop(None)
    logging.info('end captcha-solver')


async def _message_handler(event: events.NewMessage.Event) -> None:
    await event_logging.log_event_information(event)
    stats.collector.inc_value('events')

    await event.message.mark_read()

    if common_states.is_captcha_message(event):
        logging.debug('is captcha event')
        await handlers.captcha_fire_handler(event)
        return

    await handlers.skip_turn_handler(event)
