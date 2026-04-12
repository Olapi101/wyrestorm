from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

from custom_components.wyrestorm_matrix.const import DOMAIN

async def test_user_flow_success(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "WyreStorm Matrix", "host": "192.168.1.50", "port": 23},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "WyreStorm Matrix"
    assert result["data"] == {"name": "WyreStorm Matrix", "host": "192.168.1.50", "port": 23}
