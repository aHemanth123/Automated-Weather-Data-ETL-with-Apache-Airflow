# 🌤️ Weather Data ETL with Apache Airflow

This project implements an **automated weather data ETL pipeline** using **Apache Airflow (v1.10.9)** and **WeatherAPI**. The DAG fetches daily weather data for selected cities, saves it in JSON/CSV format, and archives old data locally — all without requiring a database.



 
## 🎯 Project Objective

- Automate daily weather data collection using Airflow
- Use WeatherAPI to fetch weather information
- Save the data as `.json` and/or `.csv` locally
- Archive older files into a separate folder for historical tracking
 



---


## 🛠️ Tech Stack

| Tool       | Purpose                                |
|------------|----------------------------------------|
| Apache Airflow 1.10.9 | Workflow orchestration engine (via Docker) |
| WeatherAPI | Weather data source (via API Key)      |
| Python     | For ETL logic                          |
| Bash       | For file archiving                     |
| Docker     | To run Airflow environment             |
| pandas     | To transform and save data in tabular form |

 

## 📦 Folder Structure

docker-airflow-master/  
├── dags/   
│ └── airflow_weather_dag.py    
├── weather/   
│ └── raw_london_20240627.json
├── data/   
│ └── weather_london_20240627.csv
├── archive/   
│ └── weather_london_20240625.csv
├── docker-compose.yml # Docker config for Airflow


 
---

## 🔁 ETL Pipeline Workflow

### 1. `fetch_weather_data` (PythonOperator)
- Uses `requests` to call WeatherAPI for each city
- Saves results in `/usr/local/airflow/data/` as `.json` or `.csv`

### 2. `archive_old_files` (BashOperator)
- Moves existing data files into `/usr/local/airflow/archive/` using `mv` command
- Helps organize historical data cleanly


 

## 📂 DAG Schedule & Structure

- **Schedule Interval:** `@daily`
- **Start Date:** Manual or set via backfill
- **Retries:** 1 on failure
- **Tasks:**
  - `archive_old_files`
  - `fetch_weather_data`

DAG is triggered manually or scheduled to run once per day, fetching weather data and managing file storage.


 

## 🔐 API Key Setup

Register on [https://www.weatherapi.com](https://www.weatherapi.com) and get your API key.

Update your DAG file:
```python
API_KEY = "your_actual_key"
```


----


## ▶️ Running the Project

1. Clone the repository

```
git clone https://github.com/yourusername/airflow-weather-dag.git
cd airflow-weather-dag
```

2. Start Airflow via Docker Compose
```
docker-compose up -d
```
3. Access Airflow UI

Open http://localhost:8080

```
    Username: airflow

    Password: airflow
```
4. Enable and Trigger the DAG

    Open the DAG named weather_etl

    Turn the toggle to on

    Click Trigger DAG ▶️


### 📁 Output Location

| Folder     | Contents                          |
| ---------- | --------------------------------- |
| `weather/` | Raw `.json` from WeatherAPI       |
| `data/`    | Cleaned `.csv` files (final)      |
| `archive/` | Archived `.csv` files (past runs) |


### Sample Output

weather/raw_london_20240627.json

```
{
  "location": {"name": "London"},
  "current": {"temp_c": 24.5, "humidity": 56, "wind_kph": 10.2}
}
```
data/weather_london_20240627.csv

```
city,date,temp_c,humidity,wind_kph
London,2024-06-27,24.5,56,10.2
```


### Enhancements :

Add email/Slack alerts on DAG failure
