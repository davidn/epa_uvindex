import re
from datetime import datetime

import httpx

from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

HOURLY_URL = 'https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/CITY/{city}/STATE/{state}/JSON'
DAILY_URL = 'https://data.epa.gov/efservice/getEnvirofactsUVDAILY/CITY/{city}/STATE/{state}/JSON'

class EpaUvindex:
    def __init__(self, hass: HomeAssistant, city: str, state: str):
      self.httpx_client = get_async_client(hass)
      self.city = city
      self.state = state

    def _check_error(self, response):
        json = response.json()
        if response.status_code == httpx.codes.NOT_FOUND:
            raise EnvirofactsLocationError(json['error'])
        elif httpx.codes.is_error(response.status_code):
            raise EnvirofactsApiError(json['error'])
      
    def _daily_forecast(self, response):
        days = response.json()
        return days[0]['UV_INDEX']

    def _hourly_forecast(self, response):
        hours = response.json()
        hourly_forecast = []
        for e in hours:
            hourly_forecast.append({
                "uv_index": e['UV_VALUE'],
                "datetime": datetime.strptime(e['DATE_TIME'], "%B/%d/%Y %I %p")
            })
        return hourly_forecast

    async def async_get_daily_uvindex(self) -> int:
        response = await self.httpx_client.get(DAILY_URL.format(city=self.city, state=self.state))
        self._check_error(response)
        return self._daily_forecast(response)

    def get_daily_uvindex(self) -> int:
        response = httpx.get(DAILY_URL.format(city=self.city, state=self.state))
        self._check_error(response)
        return self._daily_forecast(response)

    async def async_get_hourly_uvindex(self) -> int:
        response = await self.httpx_client.get(HOURLY_URL.format(city=self.city, state=self.state))
        self._check_error(response)
        return self._hourly_forecast(response)

    def get_hourly_uvindex(self) -> int:
        response = httpx.get(HOURLY_URL.format(city=self.city, state=self.state))
        self._check_error(response)
        return self._hourly_forecast(response)
    
class EnvirofactsLocationError(HomeAssistantError):
   """Error returned by Envirofacts API."""

class EnvirofactsApiError(HomeAssistantError):
   """Error returned by Envirofacts API."""
