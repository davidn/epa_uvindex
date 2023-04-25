from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UV_INDEX
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([NoaaUVSensor()])

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor from a config entry."""
    async_add_devices([NoaaUVSensor(hass.data[DOMAIN][config_entry.entry_id])])


class NoaaUVSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "UV Index"
    _attr_native_unit_of_measurement = UV_INDEX
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, noaa_uvindex):
        self.noaa_uvindex = noaa_uvindex

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.noaa_uvindex.get_uvindex()
