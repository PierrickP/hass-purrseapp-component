"""The Purrse.app integration."""

from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import PurrseCoordinator

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type PurrseAppConfigEntry = ConfigEntry[PurrseCoordinator]  # noqa: F821

_LOGGER = logging.getLogger(__name__)


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: PurrseAppConfigEntry) -> bool:
    """Set up Purrse.app from a config entry."""

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    coordinator = PurrseCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    # entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: PurrseAppConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


# async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
#     """Reload if change option."""
#     await hass.config_entries.async_reload(entry.entry_id)
