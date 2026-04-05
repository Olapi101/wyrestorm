from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WyreStormCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: WyreStormCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WyreStormOutputSwitch(coordinator, output) for output in range(1, 9)])

class WyreStormOutputSwitch(CoordinatorEntity[WyreStormCoordinator], SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WyreStormCoordinator, output_num: int) -> None:
        super().__init__(coordinator)
        self.output_num = output_num
        self._attr_name = f"Output {output_num} Enabled"
        self._attr_unique_id = f"wyrestorm_output_{output_num}_enabled"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("mapping", {}).get(self.output_num) is not None

    @property
    def available(self) -> bool:
        return bool(self.coordinator.last_update_success)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.hass.async_add_executor_job(self.coordinator.client.switch, 1, self.output_num)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.hass.async_add_executor_job(self.coordinator.client.switch, 0, self.output_num)
        await self.coordinator.async_request_refresh()
