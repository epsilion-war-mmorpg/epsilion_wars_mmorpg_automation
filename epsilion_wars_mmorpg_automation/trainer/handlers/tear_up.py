"""Potions handlers."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.game import action, parsers
from epsilion_wars_mmorpg_automation.settings import app_settings

logger = logging.getLogger(__file__)


async def show_potions(entity: int | events.NewMessage.Event) -> None:
    """Just checking potions as first step."""
    logger.info('show potions handler')
    await action.common_actions.show_potions(entity)


async def use_potions_and_show_scrolls(event: events.NewMessage.Event) -> None:
    """Use potions and show scrolls after."""
    logger.info('Use potions handler')
    enabled_potions = app_settings.enabled_potions
    available_potions = parsers.get_potions(event.message.message)

    if app_settings.use_potions:
        for potion in available_potions:
            if potion in enabled_potions:
                await action.common_actions.execute_command(event.chat_id, potion)

    await action.common_actions.show_scrolls(event)


async def use_scrolls_and_refresh(event: events.NewMessage.Event) -> None:
    """Use scrolls and refresh after."""
    logger.info('Use scrolls handler')

    enabled_scrolls = app_settings.enabled_scrolls
    available_scrolls = parsers.get_scrolls(event.message.message)

    if app_settings.use_scrolls:
        for scroll in available_scrolls:
            if scroll in enabled_scrolls:
                await action.common_actions.execute_command(event.chat_id, scroll)

    return await action.common_actions.ping(event)
