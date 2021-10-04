"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    async_add_entities([SMXSensor()])


class SMXSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        print("Init Sensor")
        print(self)
        self._state = None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'SMX Motion Detection Sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        print("Update SMX Motion Detection Sensor")
        print(self.hass.data[DOMAIN])
        #self._state = self.hass.data[DOMAIN]['state']
