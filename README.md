# Purrse.app Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[Purrse.app](https://purrse.app) integration of Purrse.app allows you to retrieve data from your groups

**:warning: A premium subscription on Purrse.app is required to configure this integration.**

More informations on https://purrse.app/premium

## Installation

### HACS (recommended)

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pierrickp&repository=hass-purrseapp-component&category=integration)

<!-- or go to <b>Hacs</b> and search for `Flightradar24`. -->

### Manual

1. Locate the `custom_components` directory in your Home Assistant configuration directory. It may need to be created.
2. Copy the `custom_components/flightradar24` directory into the `custom_components` directory.
3. Restart Home Assistant.

## Configuration

Add integration by clicking on

[![Open your Home Assistant instance and config the Purrse.app Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=purrseapp)

During the configuration, set your *personal token* previously created on the Purrse.app App. You can create or get your token on https://purrse.app/x/account/api

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/pierrickp/hass-pursseapp-component.svg?style=for-the-badge
[commits]: https://github.com/pierrickp/hass-pursseapp-component/commits/main

[license-shield]: https://img.shields.io/github/license/pierrickp/hass-pursseapp-component.svg?style=for-the-badge
[license]: https://github.com/pierrickp/hass-pursseapp-component/LICENSE.md

[releases-shield]: https://img.shields.io/github/release/pierrickp/hass-pursseapp-component.svg?style=for-the-badge
[releases]: https://github.com/pierrickp/hass-pursseapp-component/releases
