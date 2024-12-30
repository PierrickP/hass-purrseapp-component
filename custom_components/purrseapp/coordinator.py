"""Coordinator for Purrse."""

from datetime import timedelta
import logging

from homeassistant.components.sensor import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .api import PurrseAPI

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)


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
            update_interval=SCAN_INTERVAL,
        )
        self.api = PurrseAPI(hass, config_entry.data.get("token"))

    async def async_poll_api(hass):
        """Poll API here, grab the things I need from it, and set it to data."""

        _LOGGER.debug("COORDINATOR TEST")

    async def _async_setup(self) -> None:
        """Do initialization logic."""

        _LOGGER.debug("COORDINATOR _async_setup")

    async def _async_update_data(self):
        """Refresh groups."""

        _LOGGER.debug("COORDINATOR _async_update_data")

        try:
            groups = await self.api.getGroups()

            _LOGGER.debug("COORDINATOR ICI")
            _LOGGER.debug(groups)

            for group in groups:
                # Obtenir les détails du groupe via l'API
                _LOGGER.debug(
                    'COORDINATOR self.api.getGroup(group["id"]) %s', group["id"]
                )
                group_details = await self.api.getGroup(group["id"])
                # Ajouter les détails dans l'objet (supposons que group est un dictionnaire)
                group["details"] = group_details

        except Exception as err:
            _LOGGER.error("COORDINATOR _async_update_data ERROR")
            _LOGGER.error(err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        return PurrseGroupsData(groups)
