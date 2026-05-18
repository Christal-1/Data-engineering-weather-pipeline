import sqlite3
import pandas as pd
import os
from config.config import DB_NAME
from scripts.utils import setup_logger
import logging

setup_logger()


def extract_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM weather", conn)
    conn.close()

    if df.empty:
        raise Exception("No data found in database")

    return df


def transform_data(df):
    df["temperature_c"] = df["temperature"] - 273.15

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(by="timestamp", ascending=False)

    return df


def load_data(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/transformed_weather.csv", index=False)


def main():
    try:
        df = extract_data()
        df = transform_data(df)
        load_data(df)

        logging.info("Transformation successful")

    except Exception as e:
        logging.error(f"Transformation failed: {e}")


if __name__ == "__main__":
    main()
