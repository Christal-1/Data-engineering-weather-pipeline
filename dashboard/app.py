import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Weather Dashboard")

# Title
st.title("🌦️ Live Weather Dashboard")

# Description
st.write("Real-time weather data powered by OpenWeather API")

# Load data
try:
    df = pd.read_csv("data/transformed_weather.csv")
except FileNotFoundError:
    st.error("No data found. Please run the pipeline first.")
    st.stop()

# Handle timestamp + latest data
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    df = df.drop_duplicates(subset="city")

# Round temperature for cleaner display
if "temperature_c" in df.columns:
    df["temperature_c"] = df["temperature_c"].round(2)

# Show last updated timestamp
if "timestamp" in df.columns and not df.empty:
    st.caption(f"Last updated: {df['timestamp'].iloc[0]}")

# Rename columns for better UI
df_display = df.rename(columns={
    "city": "City",
    "temperature": "Temperature (K)",
    "temperature_c": "Temperature (°C)",
    "timestamp": "Last Updated"
})

# Display table
st.subheader("Latest Weather Data")
st.dataframe(df_display)

# Chart section
st.subheader("Temperature (°C)")

if len(df_display) > 0:
    chart_df = df_display.set_index("City")
    st.bar_chart(chart_df["Temperature (°C)"])
else:
    st.warning("No data available to display.")

# Footer (optional but nice touch)
st.markdown("---")
st.caption("Built by Christal Haines 🚀")
