# WyreStorm Matrix Home Assistant Integration

Custom Home Assistant integration for WyreStorm MX-0808-HDBT-H2 family matrix switchers over TCP/Telnet.

## Features
- Config flow setup
- Per-output select entities
- Per-output enabled switch entities
- Standby / wake / reboot buttons
- Coordinator-based polling and availability

## Installation
1. Copy `custom_components/wyrestorm_matrix` into your Home Assistant `custom_components` folder, or install via HACS once published.
2. Restart Home Assistant.
3. Add the integration from **Settings > Devices & Services**.

## Notes
The command syntax is based on WyreStorm’s LAN control API family and may need minor adjustment depending on firmware response formatting.
