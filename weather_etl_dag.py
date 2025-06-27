

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator


from datetime import datetime
import requests
import json
import os
import pandas as pd

# === Configuration ===
API_KEY =  ''# Use API Key Here
CITIES = ['Delhi', 'Mumbai', 'Kottayam']
RAW_FOLDER = '/usr/local/airflow/data/weather/raw'
ARCHIVE_FOLDER = '/usr/local/airflow/data/weather/archive'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# === Task 1: Fetch weather data and save as JSON ===
def fetch_weather():
    if not os.path.exists(RAW_FOLDER):
        os.makedirs(RAW_FOLDER)

    for city in CITIES:
        url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'
        response = requests.get(url)
        data = response.json()

        filename = f'{RAW_FOLDER}/{city}_{datetime.now().strftime("%Y-%m-%d")}.json'
        with open(filename, 'w') as f:
            json.dump(data, f)

# === Task 2: Convert JSON files to a single CSV ===
def convert_to_csv():
    files = [f for f in os.listdir(RAW_FOLDER) if f.endswith('.json')]
    all_data = []

    for file in files:
        with open(os.path.join(RAW_FOLDER, file)) as f:
            data = json.load(f)
            city = data['location']['name']
            temp = data['current']['temp_c']
            humidity = data['current']['humidity']
            condition = data['current']['condition']['text']
            dt = data['location']['localtime']

            all_data.append({
                'city': city,
                'temperature_C': temp,
                'humidity': humidity,
                'condition': condition,
                'datetime': dt
            })

    if all_data:
        df = pd.DataFrame(all_data)
        output_file = os.path.join(RAW_FOLDER, f"weather_report_{datetime.now().strftime('%Y-%m-%d')}.csv")
        df.to_csv(output_file, index=False)

# === Define DAG ===
with DAG('weatherapi_data_etl',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    fetch_weather_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather
    )

    convert_json_to_csv = PythonOperator(
        task_id='convert_json_to_csv',
        python_callable=convert_to_csv
    )

    archive_old_json = BashOperator(
        task_id='archive_old_json',
        bash_command=f'mv {RAW_FOLDER}/*.json {ARCHIVE_FOLDER}/ || true'
    )

    fetch_weather_data >> convert_json_to_csv >> archive_old_json
