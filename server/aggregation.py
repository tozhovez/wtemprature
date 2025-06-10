from abc import ABC, abstractmethod
from statistics import mean, median


class BaseAggregator(ABC):
    """Abstract base class for all aggregation strategies."""
    @abstractmethod
    async def aggregate(self, data) -> float:
        """Performs an aggregation on a list of daily temperatures."""

class AvgAggregator(BaseAggregator):
    async def aggregate(self, data) -> float:
        list_data = [d.temperature for d in data]
        return mean(list_data)

class MaxAggregator(BaseAggregator):
    async def aggregate(self, data: list) -> float:
        list_data = [d.temperature for d in data]
        return max(list_data)

class MedianAggregator(BaseAggregator):
    async def aggregate(self, data) -> float:
        list_data = [d.temperature for d in data]
        return median(list_data)

# map string → class
AGGREGATORS = {
    "avg":   AvgAggregator(),
    "max":   MaxAggregator(),
    "median": MedianAggregator(),
}