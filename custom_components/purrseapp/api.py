"""Purrse.app API."""

import asyncio
import logging

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import PURRSE_API_BASE_URL

_LOGGER = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5


class PurrseAPI:
    """Purrse.app API Class."""

    base_url = PURRSE_API_BASE_URL

    def __init__(self, hass: HomeAssistant, api_token: str) -> None:
        """Init PurrseAPI class."""
        _LOGGER.info("PurrseAPI __init__ %s", api_token)
        self.hass = hass
        self._api_token = api_token
        self._headers = {"x-api-token": api_token}

    def connect(self) -> bool:
        """Connect to api."""
        if self._api_token:
            return True
        raise APIAuthError("Error connecting to api. Invalid username or password.")

    async def get_groups(self) -> list:
        """Get all groups."""
        _LOGGER.info("GET GROUPS")

        try:
            session = async_get_clientsession(self.hass)

            async with asyncio.timeout(REQUEST_TIMEOUT):
                req = await session.get(
                    self.base_url.format(path="/groups"), headers=self._headers
                )

            return await req.json()

        except TimeoutError:
            _LOGGER.error("Could not connect to Purrse API endpoint")
        except aiohttp.ClientError as e:
            _LOGGER.error("Could not connect to Purrse API endpoint: %s", e)
        except ValueError:
            _LOGGER.error("Received non-JSON data from Purrse API endpoint")
        # except vol.Invalid as err:
        #     _LOGGER.error("Received unexpected JSON from CityBikes API endpoint: %s", err)
        raise PurrseAPIRequestError

    async def get_group(self, group_id: str) -> dict:
        """Get group."""
        _LOGGER.info("GET GROUP %s", group_id)

        # return (
        #     {
        #         "id": group_id,
        #         "name": "Group 1",
        #         "device": "EUR",
        #         "users": [{"name": "pilou", "own": 42}],
        #     },
        # )
        try:
            session = async_get_clientsession(self.hass)

            async with asyncio.timeout(REQUEST_TIMEOUT):
                req = await session.get(
                    self.base_url.format(path=f"/groups/{group_id}"),
                    headers=self._headers,
                )

            return await req.json()
        except aiohttp.ClientResponseError as err:
            _LOGGER.error("Purrse API endpoint error")
            _LOGGER.error(err)
        except (TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Could not connect to Purrse API endpoint")
        except ValueError:
            _LOGGER.error("Received non-JSON data from Purrse API endpoint")
        # except vol.Invalid as err:
        #     _LOGGER.error("Received unexpected JSON from CityBikes API endpoint: %s", err)
        raise PurrseAPIRequestError


class APIAuthError(Exception):
    """Exception class for auth error."""


class APIConnectionError(Exception):
    """Exception class for connection error."""


class PurrseAPIRequestError(Exception):
    """Error to indicate a Purrse API request has failed."""
