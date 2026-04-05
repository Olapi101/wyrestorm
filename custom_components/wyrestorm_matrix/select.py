from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WyreStormCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: WyreStormCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WyreStormOutputSelect(coordinator, output) for output in range(1, 9)])

class WyreStormOutputSelect(CoordinatorEntity[WyreStormCoordinator], SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WyreStormCoordinator, output_num: int) -> None:
        super().__init__(coordinator)
        self.output_num = output_num
        self._attr_name = f"Output {output_num} Input"
        self._attr_unique_id = f"wyrestorm_output_{output_num}_select"
        self._attr_options = [f"Input {i}" for i in range(1, 9)]

    @property
    def current_option(self):
        inp = self.coordinator.data.get("mapping", {}).get(self.output_num)
        return f"Input {inp}" if inp else None

    @property
    def available(self) -> bool:
        return bool(self.coordinator.last_update_success)

    async def async_select_option(self, option: str) -> None:
        input_num = int(option.split()[-1])
        await self.coordinator.hass.async_add_executor_job(self.coordinator.client.switch, input_num, self.output_num)
        await self.coordinator.async_request_refresh()
