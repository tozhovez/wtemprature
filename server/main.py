"""
Main module for the World Temperature FastAPI application.

This module initializes the FastAPI app, defines routes for managing sessions,
and orchestrates the calculation process using the classes.
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from config import settings
from models import TopCitiesRequest
from consumer import Consumer
from storage import AsyncStorage
from producer import Producer
from weather_api import WeatherAPI
from aggregation import AGGREGATORS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
weather_api = WeatherAPI()
task_queue = asyncio.Queue()
data_storage = AsyncStorage()
task_producer = Producer(task_queue, weather_api, data_storage)
task_consumer = Consumer(task_queue, weather_api, data_storage)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

# Routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for managing the application's lifecycle.
    This function is called when the application starts and stops.
    It initializes the data storage on startup and handles any cleanup on shutdown.
    """
    asyncio.create_task(task_consumer.start())
    logging.info("Application start...")
    yield
    logging.info("Application shutdown...")

app = FastAPI(
    lifespan=lifespan,
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "docs": "/docs",
        "redoc_url" :"/redoc",
        "version": settings.PROJECT_VERSION
    }


# Error Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.post("/weather")
async def get_weather(request: TopCitiesRequest):
    agg_type = request.aggregator
    city_ids = request.city_ids
    top_n = request.top_n if request.top_n > 0 else settings.TOP_N
    if agg_type not in AGGREGATORS:
        raise HTTPException(status_code=400, detail="Unknown aggregation type")
    await task_producer.produce(city_ids, agg_type)
    await task_queue.join()
    results = await data_storage.get_results(agg_type)
    return results[:top_n]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6767)

