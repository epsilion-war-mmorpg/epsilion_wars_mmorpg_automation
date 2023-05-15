"""Shared data variables."""
import enum

RESOURCE_TYPE: str = ''
RESOURCE_COUNTERS: dict[str, int] = {}
CHARACTER_NAME: str = ''
GRINDING_LOCATION: str | None = None
REPAIR_LOCATIONS_PATH: list[str] = []
COMBO_TURN_LOCKS: dict[str, int] = {}


class FarmingState(enum.Enum):
    """Farming tool states."""

    need_repair = enum.auto()  # need repair
    to_grinding_zone = enum.auto()  # go to grinding zone


FARMING_STATE: FarmingState | None = None  # by default - continue grinding on current location
