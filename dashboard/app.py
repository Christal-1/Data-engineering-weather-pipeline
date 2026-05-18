import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weather Dashboard")

st.title("🌦️ Live Weather Dashboard")

# Load data
df = pd.read_csv("data/transformed_weather.csv")

# Handle timestamp + latest data
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    df = df.drop_duplicates(subset="city")

# ✅ Show last updated time
if "timestamp" in df.columns and not df.empty:
    st.caption(f"Last updated: {df['timestamp'].iloc[0]}")

# Display table
st.subheader("Latest Weather Data")
st.dataframe(df)

# Display chart
st.subheader("Temperature (°C)")

if len(df) > 0:
    st.bar_chart(df.set_index("city")["temperature_c"])
else:
    st.warning("No data available to display.")
