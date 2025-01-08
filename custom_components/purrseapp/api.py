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

    def __init__(self, hass: HomeAssistant, api_token: str | None) -> None:
        """Init PurrseAPI class."""
        self.hass = hass
        self._api_token = api_token
        self._headers = {"x-api-token": api_token}

    def connect(self) -> bool:
        """
        Connect to api.

        @todo @pierrickp Do a real test on the api to validate the token
        """
        if self._api_token:
            return True
        raise APIAuthError

    async def get_groups(self) -> list:
        """Get all groups."""
        try:
            session = async_get_clientsession(self.hass)

            async with asyncio.timeout(REQUEST_TIMEOUT):
                req = await session.get(
                    self.base_url.format(path="/groups"),
                    headers=self._headers,
                    raise_for_status=True,
                )

            return await req.json()

        except TimeoutError:
            _LOGGER.exception("Could not connect to Purrse API endpoint")
        except aiohttp.ClientError:
            _LOGGER.exception("Could not connect to Purrse API endpoint")
        except ValueError:
            _LOGGER.exception("Received non-JSON data from Purrse API endpoint")
        raise PurrseAPIRequestError

    async def get_group(self, group_id: str) -> dict:
        """Get group by id."""
        try:
            session = async_get_clientsession(self.hass)

            async with asyncio.timeout(REQUEST_TIMEOUT):
                req = await session.get(
                    self.base_url.format(path=f"/groups/{group_id}"),
                    headers=self._headers,
                    raise_for_status=True,
                )

            return await req.json()
        except TimeoutError:
            _LOGGER.exception("Could not connect to Purrse API endpoint")
        except aiohttp.ClientError:
            _LOGGER.exception("Could not connect to Purrse API endpoint")
        except ValueError:
            _LOGGER.exception("Received non-JSON data from Purrse API endpoint")
        raise PurrseAPIRequestError


class APIAuthError(Exception):
    """Exception class for API Auth error."""


class APIConnectionError(Exception):
    """Exception class for connection error."""


class PurrseAPIRequestError(Exception):
    """Error to indicate a Purrse API request has failed."""
