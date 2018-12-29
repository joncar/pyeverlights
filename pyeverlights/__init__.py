import logging
import aiohttp
import asyncio
import json

ZONE_1 = 1
ZONE_2 = 2

MODE_FADE = 'fa'
MODE_BLINK = 'bl'
MODE_STROBE = 'st'
MODE_CHASE = 'cf'
MODE_REVERSE_CHASE = 'cr'
MODE_WIPE = 'wi'
MODE_RANDOM = 'ra'
MODE_TWINKLE = 'tw'
MODE_RB = 'rb'

_LOGGER = logging.getLogger(__name__)


class ConnectionError(Exception):
    pass


class EverLights:
    def __init__(self, ip, session=None):
        self._ip = ip
        self._session = session
        self._auto_session = False

    async def _fetch(self, path, params=None):
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._auto_session = True

        try:
            async with self._session.get('http://'+self._ip+path,
                                         params=params) as response:
                data = await response.json()
                _LOGGER.debug(str(response.url) + ' response: ' +
                              json.dumps(data, sort_keys=True, indent=4))
                return data
        except aiohttp.client_exceptions.ClientConnectorError as e:
            raise ConnectionError from e
        except asyncio.TimeoutError as e:
            raise ConnectionError from e
        except json.decoder.JSONDecodeError as e:
            raise ConnectionError from e

    async def get_status(self):
        resp = await self._fetch('/status/get')
        return resp

    async def set_pattern(self, channel, colors=[], modes={}):
        data = {
            'len': len(colors),
            'ptrn': colors,
            'modes': modes,
            'name': ''
        }
        await self._fetch('/ptrn/set', {
            'channel': channel,
            'data': json.dumps(data)
        })

    async def set_pattern_by_id(self, channel, id):
        data = await self.get_pattern(id)
        await self._fetch('/ptrn/set', {
            'channel': channel,
            'data': json.dumps(data)
        })
        return data['ptrn']

    async def clear_pattern(self, channel):
        await self._fetch('/ptrn/clear', {'channel': channel})

    async def get_all_patterns(self):
        resp = await self._fetch('/ptrn/all')
        return resp['patterns']

    async def get_pattern(self, id):
        return await self._fetch('/ptrn/get', {'id': id})

    async def close(self):
        if self._auto_session:
            await self._session.close()
            self._session = None
            self._auto_session = False
