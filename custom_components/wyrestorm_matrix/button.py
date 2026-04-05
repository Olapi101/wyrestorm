from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WyreStormCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: WyreStormCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WyreStormActionButton(coordinator, "standby"),
        WyreStormActionButton(coordinator, "wake"),
        WyreStormActionButton(coordinator, "reboot"),
    ])

class WyreStormActionButton(CoordinatorEntity[WyreStormCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WyreStormCoordinator, action: str) -> None:
        super().__init__(coordinator)
        self.action = action
        self._attr_name = action.title()
        self._attr_unique_id = f"wyrestorm_{action}"

    async def async_press(self) -> None:
        cmd = {"standby": "STANDBY", "wake": "WAKE", "reboot": "REBOOT"}[self.action]
        await self.coordinator.hass.async_add_executor_job(self.coordinator.client._send, cmd)
