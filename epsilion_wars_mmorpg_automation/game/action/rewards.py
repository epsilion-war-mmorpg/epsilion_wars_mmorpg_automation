"""Actions with daily rewards."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import REWARDS, get_buttons_flat
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def show_rewards(game_bot_id: int) -> None:
    """Call show rewards."""
    logging.info('call rewards command')
    # todo test

    await wait_for(1, 3)
    await client.send_message(
        entity=game_bot_id,
        message=REWARDS,
    )


async def catch_reward(event: events.NewMessage.Event) -> None:
    """Call catch daily reward."""
    logging.info('call get reward button')
    # todo test
    buttons = get_buttons_flat(event)
    if not buttons:
        raise InvalidMessageError('Get reward buttons not found.')

    await wait_for(1, 3)
    await client.send_message(
        entity=event.chat_id,
        message=buttons[0].text,
    )


async def select_reward_recipient(event: events.NewMessage.Event) -> None:
    """Select recipient for daily reward."""
    logging.info('select reward recipient')
    # todo test

    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Select character buttons not found.')

    await wait_for(1, 3)
    await event.message.click(0)
