from unittest.mock import AsyncMock, patch

import pytest

pytest_plugins = ("pytest_homeassistant_custom_component",)

@pytest.fixture
async def mock_wyrestorm_client():
    with patch("custom_components.wyrestorm_matrix.coordinator.WyreStormClient") as client:
        instance = client.return_value
        instance.get_mapping = AsyncMock(return_value="out1:in1 out2:in2 out3:in3")
        instance.switch = AsyncMock(return_value="OK")
        instance._send = AsyncMock(return_value="OK")
        yield instance
