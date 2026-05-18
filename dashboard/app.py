import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weather Dashboard")

st.title("🌦️ Weather Dashboard")

# Load data
df = pd.read_csv("data/transformed_weather.csv")

# Use timestamp to get latest per city
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    df = df.drop_duplicates(subset="city")

# Display table
st.subheader("Latest Weather Data")
st.dataframe(df)

# Chart
st.subheader("Temperature (°C)")
st.bar_chart(df.set_index("city")["temperature_c"])
