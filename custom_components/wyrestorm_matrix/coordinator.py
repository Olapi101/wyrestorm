from __future__ import annotations

import re
import socket
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_PORT, DEFAULT_SCAN_INTERVAL

class WyreStormClient:
    def __init__(self, host: str, port: int = DEFAULT_PORT, timeout: int = 3) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

    def _send(self, cmd: str) -> str:
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
            s.settimeout(self.timeout)
            s.sendall((cmd.strip() + "
").encode())
            data = []
            while True:
                try:
                    part = s.recv(4096)
                    if not part:
                        break
                    data.append(part)
                    if b"
" in part or b"" in part:
                        break
                except socket.timeout:
                    break
        return b"".join(data).decode(errors="ignore").strip()

    def switch(self, input_num: int, output_num: int | str) -> str:
        return self._send(f"SET SW in{input_num} {'all' if output_num == 'all' else f'out{output_num}'}")

    def get_mapping(self) -> str:
        return self._send("GET MP all")

    def standby(self) -> str:
        return self._send("STANDBY")

    def wake(self) -> str:
        return self._send("WAKE")

    def reboot(self) -> str:
        return self._send("REBOOT")

class WyreStormCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, host: str, port: int = DEFAULT_PORT) -> None:
        self.client = WyreStormClient(host, port)
        super().__init__(hass, name="wyrestorm_matrix", update_interval=DEFAULT_SCAN_INTERVAL)

    @staticmethod
    def parse_mapping(raw: str) -> dict[int, int | None]:
        mapping = {i: None for i in range(1, 9)}
        for out_s, inp_s in re.findall(r"out(\d+)\s*[:=]?\s*in(\d+)", raw, re.I):
            out, inp = int(out_s), int(inp_s)
            if 1 <= out <= 8:
                mapping[out] = inp
        return mapping

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            raw = await self.hass.async_add_executor_job(self.client.get_mapping)
            return {"raw_mapping": raw, "mapping": self.parse_mapping(raw)}
        except Exception as err:
            raise UpdateFailed(str(err)) from err
