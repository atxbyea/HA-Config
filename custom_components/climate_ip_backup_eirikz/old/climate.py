"""
Platform that offers support for IP controlled climate devices.

For more details about this platform, please refer to the repository
https://github.com/SebuZet/samsungrac

"""
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA
from homeassistant.exceptions import PlatformNotReady
from homeassistant.util.temperature import convert as convert_temperature
from homeassistant.helpers.service import extract_entity_ids
import homeassistant.helpers.entity_component
import homeassistant.helpers.config_validation as cv

from homeassistant.components.climate.const import (ATTR_MAX_TEMP, ATTR_MIN_TEMP)

from homeassistant.components.climate import (ClimateDevice, DOMAIN,
    ATTR_TARGET_TEMP_HIGH, ATTR_TARGET_TEMP_LOW, ATTR_CURRENT_TEMPERATURE,
    ATTR_SWING_MODE, ATTR_SWING_LIST, ATTR_FAN_MODE, ATTR_FAN_LIST, 
    ATTR_OPERATION_MODE, ATTR_OPERATION_LIST,  
)

from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT,
    CONF_ACCESS_TOKEN, CONF_HOST, CONF_TEMPERATURE_UNIT,
    ATTR_TEMPERATURE, ATTR_NAME, ATTR_ENTITY_ID,
    STATE_OFF, STATE_ON, 
)

from .yaml_const import (DEFAULT_CONF_CONFIG_FILE, CONF_CONFIG_FILE)

import voluptuous as vol
from datetime import timedelta
import functools as ft
import json
import logging
import time
import asyncio

from .controller import (ATTR_POWER, ClimateController, create_controller)


DEFAULT_CONF_CERT_FILE = '/home/homeassistant/.homeassistant/custom_components/climate-ip/ac14k_m.pem'
DEFAULT_CONF_TEMP_UNIT = TEMP_CELSIUS
DEFAULT_CONF_CONTROLLER = 'yaml'

CONF_CERT_FILE = 'cert_file'
CONF_DEBUG = 'debug'
CONF_CONTROLLER = 'controller'

REQUIREMENTS = ['requests>=2.21.0', 'xmljson>=0.2.0']

CLIMATE_IP_DATA = 'climate_ip_data'
ENTITIES = 'entities'
DEFAULT_CLIMATE_IP_TEMP_MIN = 16
DEFAULT_CLIMATE_IP_TEMP_MAX = 32
SERVICE_SET_CUSTOM_OPERATION = 'climate_ip_{}_set_property'
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default='PROVIDE_DEVICE_HOST_IN_CONFIGURATION_SECTION'): cv.string,
    vol.Optional(CONF_ACCESS_TOKEN, default='PROVIDE_ACCESS_TOKEN_IN_CONFIGURATION_SECTION'): cv.string,
    vol.Optional(CONF_CERT_FILE, default=DEFAULT_CONF_CERT_FILE): cv.string,
    vol.Optional(CONF_CONFIG_FILE, default=DEFAULT_CONF_CONFIG_FILE): cv.string,
    vol.Optional(CONF_TEMPERATURE_UNIT, default=DEFAULT_CONF_TEMP_UNIT): cv.string,
    vol.Optional(CONF_CONTROLLER, default=DEFAULT_CONF_CONTROLLER): cv.string,
    vol.Optional(CONF_DEBUG, default=False): cv.boolean,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    _LOGGER.info("climate_ip: async setup platform")

    try:
        device_controller = create_controller('yaml', config, _LOGGER)
    except:
        _LOGGER.error("climate_ip: error while creating controller!")
        raise
        return PlatformNotReady

    if device_controller is None:
        return PlatformNotReady

    async_add_entities([ClimateIP(device_controller)], True)

    async def async_service_handler(service):
        params = {key: value for key, value in service.data.items()
                  if key != ATTR_ENTITY_ID}

        devices = []
        entity_ids = service.data.get(ATTR_ENTITY_ID)
        if CLIMATE_IP_DATA in hass.data:
            if entity_ids:
                devices = [device for device in hass.data[CLIMATE_IP_DATA][ENTITIES] if 
                    device.entity_id in entity_ids]
            else:
                devices = hass.data[CLIMATE_IP_DATA][ENTITIES]

        update_tasks = []
        for device in devices:
            if not hasattr(device, 'async_set_custom_operation'):
                continue
            await getattr(device, 'async_set_custom_operation')(**params)
            update_tasks.append(device.async_update_ha_state(True))

        if update_tasks:
            await asyncio.wait(update_tasks, loop=hass.loop)

    if device_controller.service_schema_map is not None:
        hass.services.async_register(DOMAIN, SERVICE_SET_CUSTOM_OPERATION.format(device_controller.name), 
            async_service_handler, schema = vol.Schema(device_controller.service_schema_map))

class ClimateIP(ClimateDevice):
    """Representation of a Samsung climate device."""

    def __init__(self, rac_controller):
        self.rac = rac_controller
        #_LOGGER.setLevel(logging.INFO if rac_controller._debug else logging.ERROR)
        _LOGGER.setLevel(logging.INFO)

    @property
    def supported_features(self):
        return self.rac.supported_features

    @property
    def min_temp(self):
        t = self.rac.get_property(ATTR_MIN_TEMP)
        if t is None:
            t = DEFAULT_CLIMATE_IP_TEMP_MIN
        return convert_temperature(t, TEMP_CELSIUS, self.temperature_unit)

    @property
    def max_temp(self):
        t = self.rac.get_property(ATTR_MAX_TEMP)
        if t is None:
            t = DEFAULT_CLIMATE_IP_TEMP_MAX
        return convert_temperature(t, TEMP_CELSIUS, self.temperature_unit)

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        if self.rac.name is None:
            return 'climate_ip'
        else:
            return 'climate_ip_' + self.rac.name

    @property
    def state_attributes(self):
        attrs = self.rac.state_attributes
        attrs.update(super(ClimateIP, self).state_attributes)
        return attrs

    async def async_update(self):
        time.sleep(1.5)
        self.rac.update_state()

    @property
    def temperature_unit(self):
        return self.rac.temperature_unit

    @property
    def current_temperature(self):
        return self.rac.get_property(ATTR_CURRENT_TEMPERATURE)

    @property
    def target_temperature(self):
        return self.rac.get_property(ATTR_TEMPERATURE)

    @property
    def target_temperature_step(self):
        return int(1)

    @property
    def target_temperature_high(self):
        return self.rac.get_property(ATTR_TARGET_TEMP_HIGH)

    @property
    def target_temperature_low(self):
        return self.rac.get_property(ATTR_TARGET_TEMP_LOW)

    @property
    def current_operation(self):
        return self.rac.get_property(ATTR_OPERATION_MODE)

    @property
    def operation_list(self):
        return self.rac.get_property(ATTR_OPERATION_LIST)

    @property
    def is_on(self):
        return self.rac.is_on

    @property
    def current_fan_mode(self):
        return self.rac.get_property(ATTR_FAN_MODE)

    @property
    def fan_list(self):
        return self.rac.get_property(ATTR_FAN_LIST)

    def set_temperature(self, **kwargs):
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            self.rac.set_property(ATTR_TEMPERATURE, convert_temperature(
                int(kwargs.get(ATTR_TEMPERATURE)), self.temperature_unit, TEMP_CELSIUS))
        if kwargs.get(ATTR_TARGET_TEMP_HIGH) is not None:
            self.rac.set_property(ATTR_TARGET_TEMP_HIGH, convert_temperature(
                int(kwargs.get(ATTR_TARGET_TEMP_HIGH)), self.temperature_unit, TEMP_CELSIUS))
        if kwargs.get(ATTR_TARGET_TEMP_LOW) is not None:
            self.rac.set_property(ATTR_TARGET_TEMP_LOW, convert_temperature(
                int(kwargs.get(ATTR_TARGET_TEMP_LOW)), self.temperature_unit, TEMP_CELSIUS))
        self.schedule_update_ha_state(True)

    def set_swing_mode(self, swing_mode):
        self.rac.set_property(ATTR_SWING_MODE, swing_mode)
        self.schedule_update_ha_state(True)

    def set_fan_mode(self, fan_mode):
        self.rac.set_property(ATTR_FAN_MODE, fan_mode)
        self.schedule_update_ha_state(True)

    def set_operation_mode(self, operation_mode):
        self.rac.set_property(ATTR_OPERATION_MODE, operation_mode)
        self.schedule_update_ha_state(True)

    @property
    def current_swing_mode(self):
        return self.rac.get_property(ATTR_SWING_MODE)

    @property
    def swing_list(self):
        return self.rac.get_property(ATTR_SWING_LIST)

    def turn_on(self):
        self.rac.set_property(ATTR_POWER, STATE_ON)
        self.schedule_update_ha_state(True)

    def turn_off(self):
        self.rac.set_property(ATTR_POWER, STATE_OFF)
        self.schedule_update_ha_state(True)

    def set_custom_operation(self, **kwargs):
        """Set custom device mode to specified value."""
        # first, turn device on if requested
        for key, value in kwargs.items():
            if key == 'debug':
                _LOGGER.info("custom operation, setting property {} to {}".format(key, value))
                self.rac.set_debug(value)

        for key, value in kwargs.items():
            if key == ATTR_POWER and value == STATE_ON:
                _LOGGER.info("custom operation, setting property {} to {}".format(key, value))
                if not self.rac.set_property(key, value):
                    _LOGGER.error("ERROR setting property {} to {}".format(key, value))

        for key, value in kwargs.items():
            if key != ATTR_POWER:
                _LOGGER.info("custom operation, setting property {} to {}".format(key, value))
                if not self.rac.set_property(key, value):
                    _LOGGER.error("ERROR setting property {} to {}".format(key, value))

        # at the end turn device off if requested
        for key, value in kwargs.items():
            if key == ATTR_POWER and value == STATE_OFF:
                _LOGGER.info("custom operation, setting property {} to {}".format(key, value))
                if not self.rac.set_property(key, value):
                    _LOGGER.error("ERROR setting property {} to {}".format(key, value))

        self.schedule_update_ha_state(True)

    def async_set_custom_operation(self, **kwargs):
        return self.hass.async_add_job(
            ft.partial(self.set_custom_operation, **kwargs))

    async def async_added_to_hass(self):
        if CLIMATE_IP_DATA not in self.hass.data:
            self.hass.data[CLIMATE_IP_DATA] = {}
            self.hass.data[CLIMATE_IP_DATA][ENTITIES] = []
        self.hass.data[CLIMATE_IP_DATA][ENTITIES].append(self)

    async def async_will_remove_from_hass(self):
        if CLIMATE_IP_DATA  in self.hass.data:
            self.hass.data[CLIMATE_IP_DATA].remove(self)
