import asyncio
from weather_api import WeatherAPI
from aggregation import AGGREGATORS
from storage import AsyncStorage

class Consumer:
    def __init__(self,
                 queue: asyncio.Queue,
                 weather_api: WeatherAPI,
                 storage: AsyncStorage):
        self._queue = queue
        self._api = weather_api
        self._storage = storage

    async def start(self):
        while True:
            city_id, agg_type = await self._queue.get()
            try:
                # Save each City object to storage for later retrieval
                temps = self._api.getLastYearTemperature(city_id)
                agg = AGGREGATORS[agg_type]
                value = await agg.aggregate(temps)
                await self._storage.update(city_id, agg_type, value)
            finally:
                self._queue.task_done()
