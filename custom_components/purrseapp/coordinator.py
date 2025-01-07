"""Coordinator for Purrse."""

import logging
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PurrseAPI
from .const import COORDINATOR_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class PurrseGroupsData:
    """Class to hold api data."""

    groups: list[dict[str, str]]


class PurrseCoordinator(DataUpdateCoordinator):
    """Defne an object to fetch data."""

    data: PurrseGroupsData

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Class to manage fetching data API."""
        _LOGGER.debug("COORDINATOR __init__")

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=COORDINATOR_UPDATE_INTERVAL,
        )
        _LOGGER.debug("update_interval: %s", self.update_interval)
        _LOGGER.debug("always_update: %s", self.always_update)
        self.api = PurrseAPI(hass, config_entry.data.get("token"))

    async def async_poll_api(hass) -> None:
        """Poll API here, grab the things I need from it, and set it to data."""
        _LOGGER.debug("COORDINATOR TEST")

    async def _async_setup(self) -> None:
        """Do initialization logic."""
        _LOGGER.debug("COORDINATOR _async_setup")

    async def _async_update_data(self) -> PurrseGroupsData:
        """Refresh groups."""
        _LOGGER.debug("COORDINATOR _async_update_data")

        try:
            groups = await self.api.get_groups()

            _LOGGER.debug("COORDINATOR ICI")
            _LOGGER.debug(groups)

            for group in groups:
                # Obtenir les détails du groupe via l'API
                _LOGGER.debug(
                    'COORDINATOR self.api.get_group(group["id"]) %s', group["id"]
                )
                group_details = await self.api.get_group(group["id"])
                # Ajouter les détails dans l'objet (supposons que group est un dictionnaire)
                group["details"] = group_details

        except Exception as err:
            _LOGGER.error("COORDINATOR _async_update_data ERROR")
            _LOGGER.error(err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        return PurrseGroupsData(groups)
