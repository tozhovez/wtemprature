from datetime import date
from typing import Set, List, Callable, Tuple, Dict
from pydantic import BaseModel, Field, validator


class TopCitiesRequest(BaseModel):
    city_ids: Set[str] = Field(..., description="Set of city identifiers")
    aggregator: str = Field(..., description="Aggregation type: avg, max, min, median")
    top_n: int = Field(..., description="Number of top cities to return")

    @validator("aggregator")
    def validate_aggregation_type(cls, v):
        allowed = {"avg", "max", "median"}
        if v not in allowed:
            raise ValueError(f"Aggregation type must be one of {allowed}")
        return v

    @validator("top_n")
    def validate_top_n(cls, v):
        if v < 0:
            raise ValueError("top_n must be positive or 0")
        return v

