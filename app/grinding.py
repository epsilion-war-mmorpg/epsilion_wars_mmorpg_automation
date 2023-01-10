"""Seek mobs and kill them."""
import asyncio
import logging
import time

from telethon import events, types

from app.actions import complete_battle, ping, search_enemy, select_defence_direction
from app.message_parsers import is_died_state, is_hp_full_message, is_hunting_ready_message, is_win_state, \
    parse_hp_level, is_selector_defence_direction
from app.settings import app_settings
from app.telegram_client import client


async def main(execution_limit_minutes: int | None = None) -> None:
    logging.info('start grinding (%d)', execution_limit_minutes)
    logging.info('move u character to hunting location first')

    me = await client.get_me()
    logging.info('auth as %s', me.username)

    game_user: types.InputPeerUser = await client.get_input_entity(app_settings.game_username)
    logging.debug('game user is %s', game_user)

    client.add_event_handler(
        callback=_grind_handler,
        event=events.NewMessage(
            incoming=True,
            from_users=(game_user.user_id,),
        ),
    )

    await ping(game_user.user_id)

    await _run_wait_loop(execution_limit_minutes)
    logging.info('end grinding by time left')


async def _run_wait_loop(execution_limit_minutes: int | None) -> None:
    start_time = time.time()
    execution_time = 0.0
    time_limit = (execution_limit_minutes or 0) * 60

    while not time_limit or execution_time < time_limit:
        await asyncio.sleep(10)
        logging.debug('next iteration')
        execution_time = time.time() - start_time


async def _grind_handler(event: events.NewMessage.Event) -> None:
    message_content = event.message.message
    logging.info('handle event %s', message_content[:200].strip())

    if is_hunting_ready_message(message_content):
        logging.info('is ready for hunting message')
        hp_level_percent = parse_hp_level(message_content)
        logging.info('current HP level is %d%%', hp_level_percent)
        if hp_level_percent >= app_settings.minimum_hp_level_for_grinding:
            await search_enemy(event)

    elif is_hp_full_message(message_content):
        logging.info('is full HP message')
        await search_enemy(event)

    # elif is_selector_attack_direction(event):
    #     await select_attack_direction(event)

    elif is_selector_defence_direction(event):
        await select_defence_direction(event)

    # elif is_selector_special_attack(event):
    #     await select_special_attack()

    elif is_win_state(event):
        logging.info('is win state')
        await complete_battle(event)

    elif is_died_state(event):
        logging.info('is died state')
        raise RuntimeError('U died :RIP:')

    else:
        logging.debug('skip event')


if __name__ == '__main__':
    # todo getopt timelimit
    # todo getopt debug
    max_time = 10

    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    with client:
        client.loop.run_until_complete(main(max_time))
