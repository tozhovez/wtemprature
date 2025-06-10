from dataclasses import dataclass
from datetime import date, timedelta
from faker import Faker
import random
import csv
from typing import List, Tuple

@dataclass
class City:
    id: str
    name: str
    population: int

@dataclass
class DailyTemp:
    date: date
    temperature: float

def generate_city_dummy_data(num_cities: int = 10) -> List[City]:
    fake = Faker()
    cities = []
    used_ids = set()

    for _ in range(num_cities):
        name = fake.city()
        # Generate unique ID: first three letters of name, uppercase, with counter if needed
        base_id = name[:3].upper()
        id_suffix = ""
        counter = 1
        while base_id + id_suffix in used_ids:
            id_suffix = str(counter)
            counter += 1
        city_id = base_id + id_suffix
        used_ids.add(city_id)
        # Generate population (10,000 to 10,000,000)
        population = random.randint(10000, 10000000)
        cities.append(City(id=city_id, name=name, population=population))
    
    return cities

def generate_dailytemp_dummy_data(
    indx: int, num_days: int = 365
    ) -> List[DailyTemp]:
    fake = Faker()
    daily_temps = []
    # Define temperature ranges based on city index (simulating different climates)
    temp_ranges = [
        (15.0, 35.0),  # Warm climate
        (-10.0, 30.0), # Temperate
        (0.0, 25.0),   # Cool
        (-5.0, 30.0),  # Mixed
        (10.0, 40.0),  # Hot
        (0.0, 30.0),   # Arbitrary
        (-15.0, 25.0), # Cold
        (5.0, 35.0),   # Warm
        (-20.0, 20.0), # Very cold
        (10.0, 30.0),  # Mild
    ]

    # Calculate date range (June 9, 2024, to June 8, 2025)
    end_date = date(2025, 6, 8)  # One day before today (June 9, 2025)
    start_date = end_date - timedelta(days=num_days - 1)


    # Use modulo to cycle through temp_ranges if fewer than num_cities
    temp_min, temp_max = temp_ranges[indx % len(temp_ranges)]
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        # Generate random temperature within the city's range
        temperature = round(random.uniform(temp_min, temp_max), 1)
        daily_temps.append(DailyTemp(date=current_date, temperature=temperature))
    return daily_temps

def save_cities_to_csv(
    cities: List[City],
    filename: str = "configs-storage/server/infra/cities.csvcities.csv"
    ):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["id", "name", "population"])
        # Write city data
        for city in cities:
            writer.writerow([city.id, city.name, city.population])

def save_dailytemp_to_csv(
    daily_temps: List[DailyTemp], filename: str = "daily_temps.csv"
    ):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["date", "temperature"])
        # Write temperature data
        for daily_temp in daily_temps:
            writer.writerow([daily_temp.date.isoformat(), daily_temp.temperature])

if __name__ == "__main__":
    # Generate 2000 cities
    dummy_cities = generate_city_dummy_data(2000)
    # Save to CSV files
    save_cities_to_csv(dummy_cities, "configs-storage/server/infra/cities.csvcities.csv")
    print(f"Generated {len(dummy_cities)} cities and saved to cities.csv")
    
    for idx, city in enumerate(dummy_cities):
        # Generate temperature data for 365 days
        dummy_temps = generate_dailytemp_dummy_data(idx, 730)
        # Save to CSV files
        save_dailytemp_to_csv(dummy_temps, f"configs-storage/server/infra/daily_temps/{city.id}.csv")
        print(f"Generated {len(dummy_temps)} temperature records and saved to daily_temps/{city.id}.csv")