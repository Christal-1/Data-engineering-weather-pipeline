import requests
import sqlite3
from datetime import datetime
from config.config import API_KEY, CITY, DB_NAME
from scripts.utils import setup_logger
import logging

# Setup logging
setup_logger()


def fetch_weather():
    """Fetch weather data from OpenWeather API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
        response = requests.get(url, timeout=10)  # add timeout

        data = response.json()

        # Validate response properly
        if response.status_code != 200 or "main" not in data:
            raise Exception(f"API Error: {data}")

        return data

    except Exception as e:
        logging.error(f"Fetch failed: {e}")
        raise


def save_to_db(city, temp):
    """Save weather data into SQLite database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature REAL,
            timestamp TEXT
        )
        """)

        cursor.execute(
            "INSERT INTO weather VALUES (?, ?, ?)",
            (city, temp, datetime.now().isoformat())
        )

        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise


def main():
    """Main ingestion pipeline"""
    try:
        data = fetch_weather()
        temp = data["main"]["temp"]

        save_to_db(CITY, temp)

        logging.info("Data ingestion successful")

    except Exception as e:
        logging.error(f"Ingestion failed: {e}")


if __name__ == "__main__":
    main()
