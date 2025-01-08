"""Sensors for Purrse.app integration."""

import re
from typing import cast

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import (
    PurrseCoordinator,
    PurrseGroup,
    PurrseGroupMember,
    PurrseGroupsData,
)


def to_valid_entity_name(string: str | None) -> str | None:
    """
    Convertit une chaîne en un nom d'entité valide pour Home Assistant.

    :param string: La chaîne à convertir.
    :return: Une version valide de la chaîne.
    """
    if string is None:
        return None

    string = string.lower()
    string = re.sub(r"[^a-z0-9_]", "_", string)

    if not string[0].isalpha():
        string = f"entity_{string}"

    return re.sub(r"_+", "_", string).strip("_")


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sensors."""
    coordinator = config_entry.runtime_data

    entities = [
        GroupExpensesTotalSensor(coordinator, group)
        for group in coordinator.data.groups
    ]

    member_entities = [
        GroupMemberSensor(coordinator, group, member)
        for group in coordinator.data.groups
        for member in group["details"]["members"]
    ]

    async_add_entities(entities + member_entities)


class GroupExpensesTotalSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Group Total Expenses."""

    def __init__(
        self,
        coordinator: PurrseCoordinator,
        group_entry_infos: PurrseGroupMember,
    ) -> None:
        """Initisalisation de notre entité."""
        super().__init__(coordinator)

        self._group_entry_infos = group_entry_infos
        self._group_id = group_entry_infos.get("id")

        self._attr_name = f"{group_entry_infos.get('name')} Total expenses"
        self._attr_device_info = {
            "identifiers": {
                (DOMAIN, f"{to_valid_entity_name(group_entry_infos.get('name'))}")
            },
            "name": group_entry_infos.get("name"),
        }
        self._attr_unique_id = (
            f"{to_valid_entity_name(group_entry_infos.get('name'))}_expenses_total"
        )
        self._attr_has_entity_name = True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        groups = cast(PurrseGroupsData, self.coordinator.data).groups

        if groups is not None:
            group = next(
                (group for group in groups if group.get("id") == self._group_id),
                None,
            )

            if group is not None:
                self._group_entry_infos = group
                self.async_write_ha_state()

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        total = (
            self._group_entry_infos.get("details", {})
            .get("stats", {})
            .get("expenses", {})
            .get("total", 0)
        )

        return total / 100

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
        return self._group_entry_infos.get("default_currency")


class GroupMemberSensor(CoordinatorEntity, SensorEntity):
    """
    Sensor for a group's member.

    Create a sensor per member for each groups with their current balance
    """

    def __init__(
        self,
        coordinator: PurrseCoordinator,
        group_entry_infos: PurrseGroup,
        member_entry_infos: PurrseGroupMember,
    ) -> None:
        """Initisalisation de notre entité."""
        super().__init__(coordinator)

        self._member_entry_infos = member_entry_infos
        self._member_id = member_entry_infos.get("id")
        self._group_entry_infos = group_entry_infos
        self._group_id = group_entry_infos.get("id")

        name_or_email = member_entry_infos.get("name", member_entry_infos.get("email"))
        self._attr_name = f"{group_entry_infos.get("name")}" f" {name_or_email}" f" Owe"
        self._attr_device_info = {
            "identifiers": {
                (
                    DOMAIN,
                    f"{to_valid_entity_name(group_entry_infos.get('name'))}",
                )
            },
            "name": group_entry_infos.get("name"),
        }
        self._attr_unique_id = (
            f"{to_valid_entity_name(group_entry_infos.get('name'))}"
            f"_{to_valid_entity_name(name_or_email)}"
            f"_owe"
        )
        self._attr_has_entity_name = True
        self._attr_default_currency = group_entry_infos.get("default_currency")
        self._attr_native_value = member_entry_infos.get("owe") / 100

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        groups = cast(PurrseGroupsData, self.coordinator.data).groups

        if groups is not None:
            group = next(
                (group for group in groups if group.get("id") == self._group_id),
                None,
            )

            if group is not None:
                self._group_entry_infos = group
                member = next(
                    (
                        member
                        for member in group.get("details").get("members")
                        if member.get("id") == self._member_id
                    ),
                    None,
                )

                if member is not None:
                    self._member_entry_infos = member

                    self.async_write_ha_state()

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        owe = self._member_entry_infos.get("owe", 0)

        return owe / 100

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
