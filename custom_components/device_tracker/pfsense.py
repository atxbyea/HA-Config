"""
Support for the pfSense platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.pfsense/
"""
import asyncio
import logging

from homeassistant.components.http import HomeAssistantView
from homeassistant.components.device_tracker import DeviceScanner

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['http']


class PfsenseDeviceScanner(DeviceScanner):
    """This class parses output from 'arp -a' on pfSense."""

    def __init__(self):
        """Initialize the scanner."""
        self.last_results = {}

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        return self.last_results.keys()

    def get_device_name(self, device):
        """Return the provided device's name."""
        return self.last_results.get(device)

    def set_results(self, clients):
        self.last_results = clients


class PfsenseView(HomeAssistantView):
    """View to handle pfSense requests."""

    url = '/api/pfsense'
    name = 'api:pfsense'
    requires_auth = False

    def __init__(self, scanner):
        """Initialize pfSense URL endpoints."""
        self.scanner = scanner

    @asyncio.coroutine
    def post(self, request):
        """Received message from pfSense."""
        data = yield from request.post()
        file_contents = data['data'].file.read().decode("utf-8")
        _LOGGER.debug(file_contents)
        self.scanner.set_results(_parse_post_data(file_contents))


# pylint: disable=unused-argument
def get_scanner(hass, config):
    """
    Set up an endpoint for the pfSense application.
    Return a scanner.
    """
    scanner = PfsenseDeviceScanner()
    hass.http.register_view(PfsenseView(scanner))
    return scanner


def _parse_post_data(file_contents):
    # Body comes back as one string
    # each entry ends with a ]
    clients = {}
    for entry in file_contents.split("\n"):
        split_entry = entry.split()
        # Non-interface entries have 11 fields
        if len(split_entry) != 11:
            continue
        hostname = split_entry[0]
        mac = split_entry[3].upper()
        _LOGGER.debug(mac)
        # ? is an unknown hostname to pfSense
        if hostname != "?":
            clients[mac] = hostname
        else:
            clients[mac] = mac.replace(":", "")
    return clients
