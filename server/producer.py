import asyncio
from dataclasses import asdict
from typing import Set
from weather_api import WeatherAPI
from storage import AsyncStorage
from config import settings

class Producer:
    def __init__(self,
                 queue: asyncio.Queue,
                 weather_api: WeatherAPI,
                 storage: AsyncStorage
                 ):
        self._queue = queue
        self._api = weather_api
        self._storage = storage

    async def produce(self, city_ids: Set[str], agg_type: str):
        cities = self._api.getAllCitiesByIds(city_ids)
        for cid in cities:
            # Fetch city metadata from the WeatherAPI
            city_dict = asdict(cid)
            await self._storage.save(cid.id, city_dict)
            if cid.population >= settings.MIN_POPULATION:
                await self._queue.put((cid.id, agg_type))
