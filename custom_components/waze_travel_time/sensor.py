from datetime import timedelta
import logging
import re

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_REGION, EVENT_HOMEASSISTANT_START,
    ATTR_LATITUDE, ATTR_LONGITUDE, CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import location
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['https://github.com/kovacsbalu/WazeRouteCalculator/archive/04e9e9485ce61465dec6bebff1d9e987154abe6b.zip#WazeRouteCalculator==0.9.1b0']

_LOGGER = logging.getLogger(__name__)

ATTR_DURATION = 'duration'
ATTR_DISTANCE = 'distance'
ATTR_ROUTE = 'route'

ATTRIBUTION = "Powered by Waze"

CONF_DESTINATION = 'destination'
CONF_ORIGIN = 'origin'
CONF_INCL_FILTER = 'incl_filter'
CONF_EXCL_FILTER = 'excl_filter'
CONF_REALTIME = 'realtime'
CONF_UNITS = 'units'
CONF_VEHICLE_TYPE = 'vehicle_type'

DEFAULT_NAME = 'Waze Travel Time'
DEFAULT_REALTIME = False
DEFAULT_VEHICLE_TYPE = 'car'

ICON = 'mdi:car'

UNITS = [CONF_UNIT_SYSTEM_METRIC, CONF_UNIT_SYSTEM_IMPERIAL]

REGIONS = ['US', 'NA', 'EU', 'IL', 'AU']
VEHICLE_TYPES = ['car', 'taxi', 'motorcycle']

SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ORIGIN): cv.string,
    vol.Required(CONF_DESTINATION): cv.string,
    vol.Required(CONF_REGION): vol.In(REGIONS),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_INCL_FILTER): cv.string,
    vol.Optional(CONF_EXCL_FILTER): cv.string,
    vol.Optional(CONF_REALTIME, default=DEFAULT_REALTIME): cv.boolean,
    vol.Optional(CONF_VEHICLE_TYPE,
                 default=DEFAULT_VEHICLE_TYPE): vol.In(VEHICLE_TYPES),
    vol.Optional(CONF_UNITS): vol.In(UNITS)
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Waze travel time sensor platform."""
    destination = config.get(CONF_DESTINATION)
    name = config.get(CONF_NAME)
    origin = config.get(CONF_ORIGIN)
    region = config.get(CONF_REGION)
    incl_filter = config.get(CONF_INCL_FILTER)
    excl_filter = config.get(CONF_EXCL_FILTER)
    realtime = config.get(CONF_REALTIME)
    vehicle_type = config.get(CONF_VEHICLE_TYPE)
    units = config.get(CONF_UNITS)

    if units is None:
        units = hass.config.units.name

    data = WazeTravelTimeData(None, None, region, incl_filter,
                              excl_filter, realtime, units,
                              vehicle_type)

    sensor = WazeTravelTime(name, origin, destination, data)

    add_entities([sensor])

    # Wait until start event is sent to load this component.
    hass.bus.listen_once(
        EVENT_HOMEASSISTANT_START, lambda _: sensor.update())


def _get_location_from_attributes(state):
    """Get the lat/long string from an states attributes."""
    attr = state.attributes
    return '{},{}'.format(attr.get(ATTR_LATITUDE), attr.get(ATTR_LONGITUDE))


class WazeTravelTime(Entity):
    """Representation of a Waze travel time sensor."""

    def __init__(self, name, origin, destination, waze_data):
        """Initialize the Waze travel time sensor."""
        self._name = name
        self._waze_data = waze_data
        self._state = None
        self._origin_entity_id = None
        self._destination_entity_id = None

        # Attempt to find entity_id without finding address with period.
        pattern = "(?<![a-zA-Z0-9 ])[a-z_]+[.][a-zA-Z0-9_]+"

        if re.fullmatch(pattern, origin):
            _LOGGER.debug("Found origin source entity %s", origin)
            self._origin_entity_id = origin
        else:
            self._waze_data.origin = origin

        if re.fullmatch(pattern, destination):
            _LOGGER.debug("Found destination source entity %s", destination)
            self._destination_entity_id = destination
        else:
            self._waze_data.destination = destination

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._waze_data.duration is not None:
            return round(self._waze_data.duration)

        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'min'

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        if self._waze_data.duration is None:
            return None

        res = {ATTR_ATTRIBUTION: ATTRIBUTION}
        res[ATTR_DURATION] = self._waze_data.duration
        res[ATTR_DISTANCE] = self._waze_data.distance
        res[ATTR_ROUTE] = self._waze_data.route
        return res

    def _get_location_from_entity(self, entity_id):
        """Get the location from the entity_id."""
        state = self.hass.states.get(entity_id)

        if state is None:
            _LOGGER.error("Unable to find entity %s", entity_id)
            return None

        # Check if the entity has location attributes.
        if location.has_location(state):
            _LOGGER.debug("Getting %s location", entity_id)
            return _get_location_from_attributes(state)

        # Check if device is inside a zone.
        zone_state = self.hass.states.get('zone.{}'.format(state.state))
        if location.has_location(zone_state):
            _LOGGER.debug(
                "%s is in %s, getting zone location",
                entity_id, zone_state.entity_id
            )
            return _get_location_from_attributes(zone_state)

        # If zone was not found in state then use the state as the location.
        if entity_id.startswith('sensor.'):
            return state.state

        # When everything fails just return nothing.
        return None

    def _resolve_zone(self, friendly_name):
        """Get a lat/long from a zones friendly_name."""
        states = self.hass.states.all()
        for state in states:
            if state.domain == 'zone' and state.name == friendly_name:
                return _get_location_from_attributes(state)

        return friendly_name

    def update(self):
        """Fetch new state data for the sensor."""
        _LOGGER.debug("Fetching Route for %s", self._name)
        # Get origin latitude and longitude from entity_id.
        if self._origin_entity_id is not None:
            self._waze_data.origin = self._get_location_from_entity(
                self._origin_entity_id)

        # Get destination latitude and longitude from entity_id.
        if self._destination_entity_id is not None:
            self._waze_data.destination = self._get_location_from_entity(
                self._destination_entity_id)

        # Get origin from zone name.
        self._waze_data.origin = self._resolve_zone(
            self._waze_data.origin)

        # Get desination from zone name.
        self._waze_data.destination = self._resolve_zone(
            self._waze_data.destination)

        self._waze_data.update()


class WazeTravelTimeData():
    """WazeTravelTime Data object."""

    def __init__(self, origin, destination, region, include, exclude,
                 realtime, units, vehicle_type):
        """Set up WazeRouteCalculator."""
        import WazeRouteCalculator

        self._calc = WazeRouteCalculator

        self.origin = origin
        self.destination = destination
        self.region = region
        self.include = include
        self.exclude = exclude
        self.realtime = realtime
        self.units = units
        self.duration = None
        self.distance = None
        self.route = None

        # Currently WazeRouteCalc only supports PRIVATE, TAXI, MOTORCYCLE.
        if vehicle_type.upper() == 'CAR':
            # Empty means PRIVATE for waze which translates to car.
            self.vehicle_type = ''
        else:
            self.vehicle_type = vehicle_type.upper()

    def update(self):
        """Update WazeRouteCalculator Sensor."""
        if self.origin is not None and self.destination is not None:
            try:
                params = self._calc.WazeRouteCalculator(
                    self.origin, self.destination, self.region,
                    self.vehicle_type, log_lvl=logging.DEBUG)
                routes = params.calc_all_routes_info(real_time=self.realtime)

                if self.include is not None:
                    routes = {k: v for k, v in routes.items() if
                              self.include.lower() in k.lower()}

                if self.exclude is not None:
                    routes = {k: v for k, v in routes.items() if
                              self.exclude.lower() in k.lower()}

                route = sorted(routes, key=(lambda key: routes[key][0]))[0]

                self.duration, distance = routes[route]

                if self.units == CONF_UNIT_SYSTEM_IMPERIAL:
                    # Convert to miles.
                    self.distance = distance / 1.609
                else:
                    self.distance = distance

                self.route = route
            except self._calc.WRCError as exp:
                _LOGGER.warning("Error on retrieving data: %s", exp)
                return
            except KeyError:
                _LOGGER.error("Error retrieving data from server")
                return
