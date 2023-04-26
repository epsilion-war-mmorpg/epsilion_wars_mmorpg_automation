"""Farming handlers."""

import logging

from telethon import events, types

from epsilion_wars_mmorpg_automation import notifications, shared_state
from epsilion_wars_mmorpg_automation.game import action, parsers
from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.trainer.handlers import grinding


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Set state as repair_call needed."""
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
    await grinding.battle_end_handler(event)


async def hp_updated_handler(event: events.NewMessage.Event) -> None:
    """Ping only if state is empty."""
    logging.info('HP updated event - farming mode {0}'.format(shared_state.FARMING_STATE))
    if shared_state.FARMING_STATE is None:
        await action.common_actions.ping(event)


async def farming_handler(event: events.NewMessage.Event) -> None:
    """Start grinding or go to repair_call."""
    shared_state.GRINDING_LOCATION = parsers.get_location_name(event.message.message)
    logging.info('Farming ready event {0} {1}'.format(
        shared_state.FARMING_STATE,
        shared_state.GRINDING_LOCATION,
    ))

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        await action.common_actions.show_map(event)
        return

    if shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        shared_state.FARMING_STATE = None

    if shared_state.FARMING_STATE is None:
        await grinding.grinding_handler(event)


async def go_to_handler(event: events.NewMessage.Event) -> None:
    """Go to based on current state."""
    logging.info('Go to event {0} {1} {2}'.format(
        shared_state.FARMING_STATE,
        shared_state.GRINDING_LOCATION,
        shared_state.REPAIR_LOCATIONS,
    ))

    buttons = get_buttons_flat(event)
    track_locations: list[types.TypeKeyboardButton] = parsers.get_city_buttons(
        buttons,
        shared_state.REPAIR_LOCATIONS,
    )
    grinding_locations: list[types.TypeKeyboardButton] = [
        button
        for button in buttons
        if shared_state.GRINDING_LOCATION.lower() in button.text.lower()
    ]
    logging.info('get track locations {0} {1}'.format(track_locations, grinding_locations))

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        await action.farming_actions.go_to(event, track_locations[0].text)

    elif shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        await action.farming_actions.go_to(
            event,
            shared_state.GRINDING_LOCATION if grinding_locations else track_locations[0].text,
        )


async def repair_or_go_to_next(event: events.NewMessage.Event) -> None:
    """Show NPC for repairing or show map for next move."""
    logging.info('Repair or go to event {0}'.format(
        shared_state.FARMING_STATE,
    ))

    location_name: str = parsers.get_location_name(event.message.message)
    is_repairman_location = any(
        repair_location in location_name
        for repair_location in app_settings.repairman_locations
    )

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        if is_repairman_location:
            await action.common_actions.show_npc(event)
        else:
            await action.common_actions.show_map(event)

    if shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        await action.common_actions.show_map(event)


async def repair_call(event: events.NewMessage.Event) -> None:
    """Call repair dialog button."""
    logging.info('Call repair button {0}'.format(
        shared_state.FARMING_STATE,
    ))

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        inline_buttons = get_buttons_flat(event)
        for number, button in enumerate(inline_buttons):
            if 'Ремонт' in button.text:
                return await event.message.click(number)


async def repairman_call(event: events.NewMessage.Event) -> None:
    """Call repairman NPC."""
    logging.info('Call repairman if needed {0}'.format(
        shared_state.FARMING_STATE,
    ))

    npc_names = get_buttons_flat(event)[:-1]
    repair_mans: list[str] = [
        npc.text
        for npc in npc_names
        if npc.text.strip() in app_settings.repairman_names
    ]
    logging.info('repair_call man names {0}'.format(repair_mans))
    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair and repair_mans:
        await action.common_actions.call_npc(event, repair_mans[0])
