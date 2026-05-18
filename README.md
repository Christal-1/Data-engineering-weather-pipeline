# Data Engineering Project

# Weather Data Engineering Pipeline

## Overview
This project is an **end-to-end automated data engineering pipeline** that collects, processes, stores, and visualizes real-time weather data.

The system ingests live data from an external API, transforms it into a usable format, stores it for historical tracking, and displays it through an interactive dashboard.


## Setup
pip install -r requirements.txt

## Configure
Add your API key in:
config/config.py

## Run Pipeline
python scripts/ingest.py
python scripts/transform.py

## Start Dashboard
streamlit run dashboard/app.py
