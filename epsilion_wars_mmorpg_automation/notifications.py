"""Desktop and other notifications."""

from desktop_notifier import DesktopNotifier, Urgency

from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client

notifier = DesktopNotifier(
    app_name=app_settings.trainer_name,
    app_icon=None,
)


async def send_desktop_notify(message: str, is_urgent: bool = False) -> None:
    """Send desktop notification."""
    if app_settings.notifications_enabled:
        await notifier.send(
            urgency=Urgency.Normal if is_urgent else Urgency.Low,
            title=app_settings.trainer_name,
            message=message,
            timeout=app_settings.desktop_notification_timeout,
        )


async def send_favorites_notify(message: str) -> None:
    """Send message to favorites chat in telegram."""
    if app_settings.favorites_enabled:
        me = await client.get_me()
        await client.send_message(
            me,
            message=message,
            parse_mode='markdown',
        )


async def send_custom_channel_notify(message: str) -> None:
    """Send message to favorites chat in telegram."""
    if app_settings.custom_channel_for_inventory:
        destination = await client.get_entity(app_settings.custom_channel_for_inventory)
        if not destination:
            raise RuntimeError('Custom notify dialog "{0}" not found'.format(
                app_settings.custom_channel_for_inventory,
            ))
        await client.send_message(
            destination,
            message=message,
            parse_mode='markdown',
        )
