import re

import httpx

from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

BULLETIN_URL = 'https://www.cpc.ncep.noaa.gov/products/stratosphere/uv_index/bulletin.txt'

class NoaaUvindex:
    def __init__(self, hass: HomeAssistant, city: str, state: str):
      self.httpx_client = get_async_client(hass)
      self.city = city
      self.state = state
      
    def _parse_response(self, response) -> int:
        text_table = response.text.split("UVI\n")[1]
        city_state_index_list = re.split(r'(?:\s\s+|\n)', text_table)
        uvindex_for_citystate = {}
        it = iter(city_state_index_list)
        while True:
            city = next(it)
            state = next(it)
            uvindex = next(it)
            if city.upper() == self.city.upper() and state.upper() == self.state.upper():
                return uvindex
        raise CityNotFound()

    async def async_get_uvindex(self) -> int:
        response = await self.httpx_client.get(BULLETIN_URL)
        return self._parse_response(response)


    def get_uvindex(self) -> int:
        response = httpx.get(BULLETIN_URL)
        return self._parse_response(response)
    
class CityStateNotFound(HomeAssistantError):
   """User specified a City/State not provided by NOAA"""
