"""The Microsoft Graph integration."""
import asyncio
from dataclasses import dataclass
from datetime import timedelta
import logging

from hagraph.api.client import GraphApiClient
from hagraph.api.provider.presence.models import PresenceResponse
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import (
    aiohttp_client,
    config_entry_oauth2_flow,
)
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import api, config_flow
from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Microsoft Graph component."""
    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Microsoft Graph from a config entry."""
    config_flow.OAuth2FlowHandler.async_register_implementation(
        hass,
        config_entry_oauth2_flow.LocalOAuth2Implementation(
            hass,
            DOMAIN,
            entry.data[CONF_CLIENT_ID],
            entry.data[CONF_CLIENT_SECRET],
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
        ),
    )
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    auth = api.AsyncConfigEntryAuth(
        aiohttp_client.async_get_clientsession(hass), session
    )

    client = GraphApiClient(auth)

    coordinator = GraphUpdateCoordinator(hass, client)
    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": GraphApiClient(auth),
        "coordinator": coordinator,
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN][entry.entry_id]["sensor_unsub"]()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


@dataclass
class PresenceData:
    """Microsoft Graph user presence data."""

    uuid: str
    availability: str
    activity: str


@dataclass
class GraphData:
    """Graph dataclass for update coordinator."""

    presence: dict[str, PresenceData]


class GraphUpdateCoordinator(DataUpdateCoordinator):
    """Store Graph Status."""

    def __init__(
        self,
        hass: HomeAssistantType,
        client: GraphApiClient,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )
        self.data: GraphData = GraphData({})
        self.client: GraphApiClient = client

    async def _async_update_data(self) -> GraphData:
        """Fetch the latest data."""

        # Update user presence
        presence_data = {}
        my_presence = await self.client.presence.get_presence()
        presence_data[my_presence.id] = _build_presence_data(my_presence)

        _LOGGER.debug("Microsoft Graph presence_data: %s", presence_data)

        return GraphData(presence_data)


def _build_presence_data(person: PresenceResponse) -> PresenceData:
    """Build presence data from a person."""

    return PresenceData(
        uuid=person.id,
        availability=person.availability,
        activity=person.activity,
    )
