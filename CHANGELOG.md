# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-04-05
### Added
- Home Assistant custom integration scaffold for WyreStorm matrix control.
- Config flow for UI-based setup.
- Coordinator-driven polling and parsed mapping state.
- Output select entities for routing inputs to outputs.
- Output enabled switch entities for quick control.
- Standby, wake, and reboot button entities.
- HACS metadata and GitHub-ready repository structure.

### Changed
- Improved entity availability handling.
- Prepared the integration for GitHub repository publication.

### Notes
- Mapping parsing may need adjustment if the matrix firmware returns a different `GET MP all` format.
