"""Shared data variables."""
import enum

RESOURCE_TYPE: str = ''
RESOURCE_COUNTERS: dict[str, int] = {}  # noqa: WPS407
CHARACTER_NAME: str = ''
GRINDING_LOCATION: str = ''


class FarmingState(enum.Enum):
    """Farming tool states."""

    need_repair = enum.auto()
    to_grinding_zone = enum.auto()


FARMING_STATE: FarmingState | None = None
