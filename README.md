
# 🌡️ Weather Aggregation System

This project is a **fully asynchronous FastAPI microservice** designed to fetch city temperature data, perform aggregations (e.g., `avg`, `max`, `median`), and return the top N results. The system uses modular components, async file I/O, and an extensible architecture ready for production.

---

## 📦 Project Structure

```
server/
├── aggregation.py              # Aggregation logic (avg, max, median)
├── config.py                   # Configuration helpers
├── consumer.py                 # Async task consumer
├── Dockerfile                  # Service container definition
├── main.py                     # FastAPI entrypoint
├── models.py                   # Data models: City, DailyTemp
├── producer.py                 # Async task producer
├── requirements.txt            # Python dependencies
├── storage.py                  # In-memory async storage
├── utils.py                    # CSV utilities (async reader)
└── weather_api.py              # WeatherAPI implementation using CSV
```

---

## 🐳 Docker Setup  

### Run application services

```bash
make run-services
```

### Stop application services

```bash
make stop-services
```

### Run infrastructure (data/config volumes)

```bash
make run-infra
```

> Volumes are mounted from:

* `${CONFIGS_STORAGE}` → `/infra`
* `${DATASTORAGE}` → `/data`

---

## ⚙️ Makefile Targets

| Command                     | Description                                   |
| --------------------------- | --------------------------------------------- |
| `make help`                 | Show available commands                       |
| `make envs`                 | Print environment variables and tools         |
| `make run-services`         | Run server in Docker with config/data volumes |
| `make stop-services`        | Stop server container                         |
| `make run-infra`            | Start infra containers                        |
| `make install-requirements` | Install Python tool dependencies              |
| `make clean`                | Clean compiled files and temporary artifacts  |
| `make list`                 | List all Makefile targets                     |


**Example**:


## 🧪 Test Data Generation

You can generate synthetic city and temperature datasets with:

```bash
python infra/generate_weather_dummy_data.py
```

This script generates:

* `configs-storage/server/infra/cities.csv`: list of 2000 fake cities
* `configs-storage/server/infra/daily_temps/{CITY_ID}.csv`: 2 years of daily temperatures per city

---

## 📁 File Tree Overview

```
configs-storage/
└── server/
    └── infra/
        ├── cities.csv
        └── daily_temps/
            ├── TLV.csv
            ├── NYC.csv
            └── ...
```

---

## 🐍 Python Requirements

Install locally with:

```bash
make install-requirements
```

Requirements include:

* `fastapi`, `uvicorn`, `aiofiles`
* `pandas`, `faker` (for data generation)
* `httpx` (if extended to external APIs)

---

### 🐳 Container Startup Logs

When running with `make run-services`, you may see a warning during container launch:

```bash
WARN[0001] could not start menu, an error occurred while starting: input/output error
Attaching to server
server  | INFO:     Started server process [1]
server  | INFO:     Waiting for application startup.
server  | INFO:root:Application start...
server  | INFO:     Application startup complete.
server  | INFO:     Uvicorn running on http://0.0.0.0:6767 (Press CTRL+C to quit)
```

---

### 🌐 API Access

Once the container is running, access the FastAPI documentation via:

📘 Swagger UI: [http://0.0.0.0:6767/docs](http://0.0.0.0:6767/docs)
📘 ReDoc: [http://0.0.0.0:6767/redoc](http://0.0.0.0:6767/redoc)

---

### ✅ Example: Health Check

**Request:**

```bash
curl -X 'GET' \
  'http://0.0.0.0:6767/' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "Welcome to The World Temperature API!",
  "docs": "/docs",
  "redoc_url": "/redoc",
  "version": "1.0.0"
}
```

---

### 📊 Example: Aggregation Request

**Request:**

```bash
curl -X 'POST' \
  'http://0.0.0.0:6767/weather' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "city_ids": [
      "JOS", "DUS", "EAS2", "POR", "SAB", "ZAC", "IVA","EAS134","EAS135", "WES149", "SAR7", "OSB"
    ],
    "aggregator": "avg",
    "top_n": 6
}'
```

**Response:**

```json
[
  {
    "id": "JOS",
    "name": "Josephton",
    "population": 4701091,
    "avg": 25.353150684931506
  },
  {
    "id": "IVA",
    "name": "Ivanborough",
    "population": 7787395,
    "avg": 19.881095890410958
  },
  {
    "id": "EAS135",
    "name": "East Anthonybury",
    "population": 6290023,
    "avg": 19.79739726027397
  },
  {
    "id": "ZAC",
    "name": "Zacharyland",
    "population": 585836,
    "avg": 19.776027397260275
  },
  {
    "id": "OSB",
    "name": "Osbornefurt",
    "population": 6437171,
    "avg": 19.502739726027396
  },
  {
    "id": "WES149",
    "name": "West Danielside",
    "population": 6494513,
    "avg": 15.032739726027398
  }
]
```



