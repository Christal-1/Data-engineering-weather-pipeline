import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

from config.config import API_KEY, CITY

st.set_page_config(page_title="Weather Dashboard")

st.title("🌦️ Live Weather Dashboard")
st.write("Real-time weather data powered by OpenWeather API")


# ✅ FETCH DATA LIVE (NO DB)
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        raise Exception(f"API Error: {data}")

    return data


try:
    data = fetch_weather()

    temp_k = data["main"]["temp"]
    temp_c = round(temp_k - 273.15, 2)

    timestamp = datetime.now()

    # ✅ Create dataframe
    df = pd.DataFrame([{
        "City": CITY,
        "Temperature (K)": temp_k,
        "Temperature (°C)": temp_c,
        "Last Updated": timestamp
    }])

    st.caption(f"Last updated: {timestamp}")

    st.subheader("Latest Weather Data")
    st.dataframe(df)

    st.subheader("Temperature (°C)")
    st.bar_chart(df.set_index("City")["Temperature (°C)"])

except Exception as e:
    st.error(f"Failed to fetch weather: {e}")


st.markdown("---")
st.caption("Built by Christal Haines 🚀")
