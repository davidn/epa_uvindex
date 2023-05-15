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
    add_entities([EpaUVSensor()])

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor from a config entry."""
    async_add_devices([EpaUVSensor(hass.data[DOMAIN][config_entry.entry_id])])


class EpaUVSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "UV Index"
    _attr_native_unit_of_measurement = UV_INDEX
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, epa_uvindex):
        self.epa_uvindex = epa_uvindex

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.epa_uvindex.get_daily_uvindex()
        self._attr_extra_state_attributes = {"forecast":self.epa_uvindex.get_hourly_uvindex()}
