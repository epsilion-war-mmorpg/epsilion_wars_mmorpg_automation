import logging

from telethon import events

from epsilion_wars_mmorpg_automation import notifications, shared_state
from epsilion_wars_mmorpg_automation.game import action, parsers
from epsilion_wars_mmorpg_automation.trainer import handlers


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Set state as repair needed."""
    logging.info('equip broken event - farming mode')
    shared_state.FARMING_STATE = shared_state.FarmingState.need_repair

    notify_message = parsers.strip_message(event.message.message)
    await notifications.send_desktop_notify(
        message=notify_message,
        is_urgent=True,
    )


async def battle_end_handler(event: events.NewMessage.Event) -> None:
    """Complete win/fail battle and ."""
    logging.info('Battle end event - farming mode {0}'.format(shared_state.FARMING_STATE))
    shared_state.FARMING_STATE = shared_state.FarmingState.to_grinding_zone
    await handlers.battle_end_handler(event)


async def hp_updated_handler(event: events.NewMessage.Event) -> None:
    """Ping only if state is empty."""
    logging.info('HP updated event - farming mode {0}'.format(shared_state.FARMING_STATE))
    if shared_state.FARMING_STATE is None:
        await action.common_actions.ping(event)


async def farming_handler(event: events.NewMessage.Event) -> None:
    """Start grinding or go to repair."""
    logging.info('Farming ready event {0}'.format(shared_state.FARMING_STATE))

    if shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        shared_state.FARMING_STATE = None

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        shared_state.GRINDING_LOCATION = parsers.get_location_name(event.message.message)
        logging.info('save grinding location name {0}'.format(shared_state.GRINDING_LOCATION))
        await action.common_actions.show_map(event)

    if shared_state.FARMING_STATE is None:
        await handlers.grinding_handler(event)


async def go_to_town_for_repair_handler(event: events.NewMessage.Event) -> None:
    """Go to town based on current state."""
    logging.info('Go to town event {0}'.format(shared_state.FARMING_STATE))
    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        await action.farming_actions.go_to_town(event)
