"""Interfaces with the Integration 101 Template api sensors."""

from datetime import timedelta
import logging
import re

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

INTERVAL_POOL_GROUPS_SECONDS = 10


def to_valid_entity_name(string):
    """Convertit une chaîne en un nom d'entité valide pour Home Assistant.

    :param string: La chaîne à convertir.
    :return: Une version valide de la chaîne.
    """

    string = string.lower()
    string = re.sub(r"[^a-z0-9_]", "_", string)

    if not string[0].isalpha():
        string = f"entity_{string}"

    return re.sub(r"_+", "_", string).strip("_")


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sensors."""

    coordinator = config_entry.runtime_data

    entities = [
        entity
        for group in coordinator.data.groups
        for entity in (
            GroupExpensesTotalSensor(hass, group),  # Première entité
            GroupOweTotalSensor(hass, group),  # Deuxième entité
        )
    ]

    # entities = [GroupExpensesTotalSensor(hass, group) for group in coordinator.data.groups]
    # pour chaque membre d'un group, creer une entité

    for group in coordinator.data.groups:
        _LOGGER.info(group["details"]["members"])

    member_entities = [
        GroupMemberSensor(hass, group, member)
        for group in coordinator.data.groups
        for member in group["details"]["members"]
    ]

    _LOGGER.info("SENSOR")
    _LOGGER.info(entities + member_entities)

    async_add_entities(entities + member_entities)


class GroupExpensesTotalSensor(SensorEntity):
    """Sensor for Group Total Expenses."""

    def __init__(
        self,
        hass: HomeAssistant,
        group_entry_infos,
    ) -> None:
        """Initisalisation de notre entité."""

        _LOGGER.info("ICI")
        _LOGGER.info(group_entry_infos)

        self._attr_name = "Total expenses"
        self._attr_device_info = {
            "identifiers": {
                (DOMAIN, f"{to_valid_entity_name(group_entry_infos.get('name'))}")
            },
            "name": group_entry_infos.get("name"),
        }
        self._attr_unique_id = (
            f"{to_valid_entity_name(group_entry_infos.get("name"))}_expenses_total"
        )
        self._attr_has_entity_name = True
        self._attr_default_currency = group_entry_infos.get("default_currency")
        self._attr_native_value = (
            group_entry_infos["details"]["stats"]["expenses"]["total"] / 100
        )

    @property
    def icon(self) -> str | None:  # noqa: D102
        return "mdi:account-group"

    @property
    def device_class(self) -> SensorDeviceClass | None:  # noqa: D102
        return SensorDeviceClass.MONETARY

    @property
    def state_class(self) -> SensorStateClass | None:  # noqa: D102
        return SensorStateClass.TOTAL

    @property
    def native_unit_of_measurement(self) -> str | None:  # noqa: D102
        return self._attr_default_currency


class GroupOweTotalSensor(SensorEntity):
    """Sensor for Group Total Expenses."""

    def __init__(
        self,
        hass: HomeAssistant,
        group_entry_infos,
    ) -> None:
        """Initisalisation de notre entité."""

        self._attr_name = "Total expenses"
        self._attr_device_info = {
            "identifiers": {
                (DOMAIN, f"{to_valid_entity_name(group_entry_infos.get("name"))}")
            },
            "name": group_entry_infos.get("name"),
        }
        self._attr_unique_id = (
            f"{to_valid_entity_name(group_entry_infos.get("name"))}_owe"
        )
        self._attr_has_entity_name = True
        self._attr_default_currency = group_entry_infos.get("default_currency")
        self._attr_native_value = group_entry_infos.get("owe") / 100

    @property
    def icon(self) -> str | None:  # noqa: D102
        return "mdi:account-group"

    @property
    def device_class(self) -> SensorDeviceClass | None:  # noqa: D102
        return SensorDeviceClass.MONETARY

    @property
    def state_class(self) -> SensorStateClass | None:  # noqa: D102
        return SensorStateClass.TOTAL

    @property
    def native_unit_of_measurement(self) -> str | None:  # noqa: D102
        return self._attr_default_currency


class GroupMemberSensor(SensorEntity):
    """Sensor for a group's member."""

    def __init__(
        self, hass: HomeAssistant, group_entry_infos, member_entry_infos
    ) -> None:
        """Initisalisation de notre entité."""

        _LOGGER.debug("SENSOR Créé un GroupMemberSensor entry=%s", group_entry_infos)
        _LOGGER.info("PLOP")
        _LOGGER.info(member_entry_infos.get("name"))

        self._attr_name = (
            f"{member_entry_infos.get('name') or member_entry_infos.get("email")} Owe"
        )
        self._attr_device_info = {
            "identifiers": {
                (
                    DOMAIN,
                    f"{to_valid_entity_name(group_entry_infos.get("name"))}",
                )
            },
            "name": group_entry_infos.get("name"),
        }
        self._attr_unique_id = f"{to_valid_entity_name(group_entry_infos.get("name"))}_{to_valid_entity_name(member_entry_infos.get("name") or member_entry_infos.get("email"))}_owe"
        self._attr_has_entity_name = True
        self._attr_default_currency = group_entry_infos.get("default_currency")
        self._attr_native_value = group_entry_infos.get("owe") / 100

    @property
    def icon(self) -> str | None:  # noqa: D102
        return "mdi:account"

    @property
    def device_class(self) -> SensorDeviceClass | None:  # noqa: D102
        return SensorDeviceClass.MONETARY

    @property
    def state_class(self) -> SensorStateClass | None:  # noqa: D102
        return SensorStateClass.TOTAL

    @property
    def native_unit_of_measurement(self) -> str | None:  # noqa: D102
        return self._attr_default_currency
