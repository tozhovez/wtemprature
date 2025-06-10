"""
Central configuration file for the application.
"""
import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    TITLE: str = "World Weather Aggregator API"
    DESCRIPTION: str = "An asynchronous API to get weather data for top N cities."
    PROJECT_NAME: str = "The World Temperature API"
    PROJECT_VERSION: str = "1.0.0"
    # The number of top cities to return in the final result
    TOP_N = 10
    # The minimum population a city must have to be included in the result
    MIN_POPULATION = 50000
    CITIES_FILE_PATH: str = "infra/cities.csv"
    TEMPERATURES_DIR: str = "infra/daily_temps"

settings = Settings()
