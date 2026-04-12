# v1.2.0 Release

This release prepares the WyreStorm Matrix Home Assistant integration for GitHub publication and installation through standard repository workflows.

## Highlights
- Config flow setup for direct Home Assistant onboarding.
- Per-output selection entities for matrix routing.
- Availability-aware state handling via a coordinator.
- Action buttons for standby, wake, and reboot.
- GitHub and HACS repository metadata included.

## Install
1. Copy `custom_components/wyrestorm_matrix` into your Home Assistant `custom_components` directory, or install through HACS once the repository is published.
2. Restart Home Assistant.
3. Add **WyreStorm Matrix** from **Settings > Devices & Services**.

## Validation
- Confirm the matrix responds to `GET MP all` over Telnet/TCP.
- Confirm `SET SW` commands match the firmware’s input/output naming.
