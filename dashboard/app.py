import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

from config.config import API_KEY, CITY

# Page config
st.set_page_config(page_title="Weather Dashboard")

# Title
st.title("🌦️ Live Weather Dashboard")
st.write("Real-time weather data powered by OpenWeather API")


# ✅ FETCH DATA LIVE (FIXED URL)
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        raise Exception(f"API Error: {data}")

    return data


try:
    # ✅ Get API data
    data = fetch_weather()

    temp_k = data["main"]["temp"]
    temp_c = round(temp_k - 273.15, 2)

    # ✅ FIX TIMEZONE (South Africa)
    sa_tz = pytz.timezone("Africa/Johannesburg")
    timestamp = datetime.now(sa_tz)

    # ✅ Create dataframe
    df = pd.DataFrame([{
        "City": CITY,
        "Temperature (K)": round(temp_k, 2),
        "Temperature (°C)": temp_c,
        "Last Updated": timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }])

    # ✅ Display timestamp
    st.caption(f"Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # ✅ Show table
    st.subheader("Latest Weather Data")
    st.dataframe(df)

    # ✅ Show chart
    st.subheader("Temperature (°C)")
    st.bar_chart(df.set_index("City")["Temperature (°C)"])


except Exception as e:
    st.error(f"Failed to fetch weather: {e}")


# Footer
st.markdown("---")
st.caption("Built by Christal Haines ")
