import streamlit as st
import pandas as pd

# ✅ Import pipeline functions directly
from scripts.ingest import main as run_ingest
from scripts.transform import main as run_transform

# Page config
st.set_page_config(page_title="Weather Dashboard")

# Title
st.title("🌦️ Live Weather Dashboard")
st.write("Real-time weather data powered by OpenWeather API")

# ✅ RUN PIPELINE PROPERLY (THIS IS THE FIX)
try:
    if "pipeline_ran" not in st.session_state:
        run_ingest()
        run_transform()
        st.session_state.pipeline_ran = True
except Exception as e:
    st.warning(f"Pipeline error: {e}")

# ✅ Load data
try:
    df = pd.read_csv("data/transformed_weather.csv")
except FileNotFoundError:
    st.error("No data found. Pipeline failed to run.")
    st.stop()

# ✅ Process data
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    df = df.drop_duplicates(subset="city")

if "temperature_c" in df.columns:
    df["temperature_c"] = df["temperature_c"].round(2)

# ✅ Show last updated
if not df.empty:
    st.caption(f"Last updated: {df['timestamp'].iloc[0]}")

# ✅ Rename for UI
df_display = df.rename(columns={
    "city": "City",
    "temperature": "Temperature (K)",
    "temperature_c": "Temperature (°C)",
    "timestamp": "Last Updated"
})

# ✅ Table
st.subheader("Latest Weather Data")
st.dataframe(df_display)

# ✅ Chart
st.subheader("Temperature (°C)")

if len(df_display) > 0:
    st.bar_chart(df_display.set_index("City")["Temperature (°C)"])
else:
    st.warning("No data available.")

# ✅ Footer
st.markdown("---")
st.caption("Built by Christal Haines 🚀")
