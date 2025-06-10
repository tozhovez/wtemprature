import asyncio
from dataclasses import asdict
from typing import Dict
from weather_api import City

class AsyncStorage:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._results = {}

    async def update(self, key_id: str, key: str, value: float):
        async with self._lock:
            self._results[key_id][key] = value

    async def save(self, key_id: str, data: dict):
        async with self._lock:
            self._results[key_id] = data

    async def get_results(self, key_id):
        async with self._lock:
            data = sorted(self._results.values(), key=lambda kv: kv[key_id], reverse=True)
            return data

    async def get_all(self):
        async with self._lock:
            return self._results.values()