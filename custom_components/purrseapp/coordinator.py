"""Coordinator for Purrse.app integration."""

import logging
from dataclasses import dataclass
from typing import TypedDict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PurrseAPI
from .const import COORDINATOR_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PurrseGroupMember(TypedDict):
    """Purrse group member type."""

    id: str
    name: str | None
    email: str | None
    owe: int


class PurrseGroupDetail(TypedDict):
    """Purrse group detail type."""

    members: list[PurrseGroupMember]


class PurrseGroup(TypedDict):
    """Purrse group type."""

    id: str
    name: str
    default_currency: str
    details: PurrseGroupDetail


@dataclass
class PurrseGroupsData:
    """Class to hold api data."""

    groups: list[PurrseGroup]


class PurrseCoordinator(DataUpdateCoordinator):
    """Define an object to fetch data."""

    data: PurrseGroupsData

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Class to manage fetching data API."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=COORDINATOR_UPDATE_INTERVAL,
        )

        self.api = PurrseAPI(hass, config_entry.data.get("token"))

    async def _async_update_data(self) -> PurrseGroupsData:
        """Refresh groups data."""
        try:
            groups = await self.api.get_groups()

            for group in groups:
                group_details = await self.api.get_group(group["id"])
                group["details"] = group_details

        except Exception as err:
            _LOGGER.exception("COORDINATOR _async_update_data ERROR")
            msg = f"Error communicating with API: {err}"

            raise UpdateFailed(msg) from err

        self.data = PurrseGroupsData(groups)

        return PurrseGroupsData(groups)
