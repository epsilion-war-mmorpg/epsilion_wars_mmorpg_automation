"""Farming handlers."""

import logging

from telethon import events, types

from epsilion_wars_mmorpg_automation import notifications, shared_state
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game import action, parsers, state
from epsilion_wars_mmorpg_automation.game.buttons import get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.trainer.handlers import grinding
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def equip_broken_handler(event: events.NewMessage.Event) -> None:
    """Set state as repair_start needed."""
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
    if shared_state.FARMING_STATE is not shared_state.FarmingState.need_repair:
        shared_state.FARMING_STATE = shared_state.FarmingState.to_grinding_zone
        await action.common_actions.call_binding(event, app_settings.equip_travel_number)
    await grinding.battle_end_handler(event)


async def hp_updated_handler(event: events.NewMessage.Event) -> None:
    """Ping only if state is empty."""
    logging.info('HP updated event - farming mode {0}'.format(shared_state.FARMING_STATE))
    if shared_state.FARMING_STATE is None:
        await action.common_actions.ping(event)


async def farming_handler(event: events.NewMessage.Event) -> None:
    """Start grinding or go to repair_start."""
    shared_state.GRINDING_LOCATION = parsers.get_location_name(event.message.message)
    logging.info('Farming ready event {0} {1}'.format(
        shared_state.FARMING_STATE,
        shared_state.GRINDING_LOCATION,
    ))

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        await action.common_actions.call_binding(event, app_settings.equip_travel_number)
        await action.common_actions.show_map(event)
        return

    if shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        shared_state.FARMING_STATE = None
        await action.common_actions.call_binding(event, app_settings.equip_farming_number)

    if state.reward_states.have_unread_message(event):
        await action.reward_actions.show_rewards(event.chat_id)
        return

    if shared_state.GRINDING_PAUSED:
        logging.info('grinding paused')
        return

    if shared_state.FARMING_STATE is None:
        await grinding.grinding_handler(event)


async def go_to_handler(event: events.NewMessage.Event) -> None:
    """Go to based on current state."""
    logging.info('Go to event {0} {1} {2}'.format(
        shared_state.FARMING_STATE,
        shared_state.GRINDING_LOCATION,
        shared_state.REPAIR_LOCATIONS_PATH,
    ))

    buttons = get_buttons_flat(event)
    track_locations: list[types.TypeKeyboardButton] = parsers.get_city_buttons(
        buttons,
        shared_state.REPAIR_LOCATIONS_PATH,
    )
    grinding_locations: list[types.TypeKeyboardButton] = [
        button
        for button in buttons
        if shared_state.GRINDING_LOCATION and shared_state.GRINDING_LOCATION.lower() in button.text.lower()
    ]
    logging.info('get track locations {0} {1}'.format(
        [location.text for location in track_locations],
        [location.text for location in grinding_locations],
    ))

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
        repair_location.lower() in location_name.lower()
        for repair_location in app_settings.repairman_locations
    )
    logging.info(f'debug {location_name} {is_repairman_location} ')

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        if is_repairman_location:
            await action.common_actions.show_npc(event)
        else:
            await action.common_actions.show_map(event)

    if shared_state.FARMING_STATE is shared_state.FarmingState.to_grinding_zone:
        await action.common_actions.show_map(event)


async def repair_start(event: events.NewMessage.Event) -> None:
    """Call repair dialog button."""
    logging.info('Call repair button {0}'.format(
        shared_state.FARMING_STATE,
    ))

    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        inline_buttons = get_buttons_flat(event)
        for number, button in enumerate(inline_buttons):
            if 'Ремонт' in button.text:
                await wait_for()
                return await event.message.click(number)


async def repairman_call(event: events.NewMessage.Event) -> None:
    """Call repairman NPC."""
    logging.info('Call repairman if needed {0}'.format(
        shared_state.FARMING_STATE,
    ))
    repair_man = _get_repairman(event)
    logging.info('repair_start man name {0}'.format(repair_man))
    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair and repair_man:
        await action.common_actions.call_npc(event, repair_man)


async def repair_item(event: events.NewMessage.Event) -> None:
    """Call repair item."""
    logging.info('Select item for repair {0}'.format(
        shared_state.FARMING_STATE,
    ))
    if shared_state.FARMING_STATE is not shared_state.FarmingState.need_repair:
        return None

    broken_items: list[tuple[int, str]] = [
        (index, button.text)
        for index, button in enumerate(get_buttons_flat(event)[:-1])
        if 'Удочка' not in button.text and parsers.get_equip_hp_level(button.text) == 0
    ]
    logging.debug('broken items found {0}'.format(broken_items))

    for index, name in broken_items:
        if parsers.get_equip_hp_max_level(name) >= app_settings.equip_minimal_hp_level_for_repairing:
            logging.info('repair item {0}'.format(name))
            await wait_for()
            return await event.message.click(index)

    shared_state.FARMING_STATE = shared_state.FarmingState.to_grinding_zone
    await action.common_actions.ping(event)


async def repair_item_approve(event: events.NewMessage.Event) -> None:
    """Approve item repair."""
    logging.info('approve item repair {0}'.format(
        shared_state.FARMING_STATE,
    ))
    if shared_state.FARMING_STATE is shared_state.FarmingState.need_repair:
        await wait_for()
        response = await event.message.click(0)
        logging.info('repair result "{0}"'.format(response))


async def skip_vendor(event: events.NewMessage.Event) -> None:
    """Skip vendor."""
    logging.info('call skip vendor dialog {0}, {1}'.format(
        app_settings.skip_random_vendor,
        app_settings.skip_random_vendor_stop_words,
    ))
    message = parsers.strip_message(event.message.message)
    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Invalid vendor buttons.')

    if app_settings.skip_random_vendor_stop_words:
        for stop_word in app_settings.skip_random_vendor_stop_words.split(','):
            if stop_word.strip().lower() in message:
                return

    if app_settings.skip_random_vendor:
        await wait_for()
        await event.message.click(len(inline_buttons) - 1)


def _get_repairman(event: events.NewMessage.Event) -> str | None:
    npc_names = get_buttons_flat(event)[:-1]

    for test_name in app_settings.repairman_names:
        for npc in npc_names:
            if test_name in npc.text.strip():
                return npc.text
    return None
