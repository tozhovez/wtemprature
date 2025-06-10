from dataclasses import dataclass
from typing import Set, List
from datetime import date, datetime
from utils import read_data_from_csv_file

@dataclass
class City:
    id: str
    name: str
    population: int

@dataclass
class DailyTemp:
    date: date
    temperature: float

class WeatherAPI:
    def getAllCitiesByIds(self, city_ids: Set[str]) -> List[City]:
        """
        Load city metadata from CSV and return only the ones requested by IDs.
        """
        cities = []

        list_of_dicts = read_data_from_csv_file("/infra/cities.csv")

        for row in list_of_dicts:
           
            if row['id'] in city_ids:
                try:
                    cities.append(City(
                        id=row['id'],
                        name=row['name'],
                        population=int(row['population'])
                    ))
                except Exception as e:
                    # You can optionally log this error
                    continue

        return cities

    def getLastYearTemperature(self, city_id: str) -> List[DailyTemp]:
        filepath = f"/infra/daily_temps/{city_id}.csv"
        list_of_dicts = read_data_from_csv_file(filepath)

        temperatures = []
        for row in list_of_dicts:
            try:
                temp = DailyTemp(
                    date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
                    temperature=float(row['temperature'])
                )
                temperatures.append(DailyTemp(
                    date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
                    temperature=float(row['temperature'])
                ))
            except Exception:
                continue
        
        return temperatures
