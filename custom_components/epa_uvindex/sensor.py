from datetime import timedelta
import logging

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

SCAN_INTERVAL = timedelta(hours=1)
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    async_add_entities([EpaUVSensor()])

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor from a config entry."""
    async_add_devices([EpaUVSensor(hass.data[DOMAIN][config_entry.entry_id])])


class EpaUVSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "UV Index"
    _attr_native_unit_of_measurement = UV_INDEX
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, epa_uvindex) -> None:
        self.epa_uvindex = epa_uvindex
        self._attr_unique_id = "{city}_{state}_uvindex".format(city=epa_uvindex.city, state=epa_uvindex.state)

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = await self.epa_uvindex.async_get_daily_uvindex()
        self._attr_extra_state_attributes = {"forecast": await self.epa_uvindex.async_get_hourly_uvindex()}
        
    async def async_added_to_hass(self) -> None:
        await self.async_update()
