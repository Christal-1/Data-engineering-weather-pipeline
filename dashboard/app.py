import streamlit as st
import pandas as pd
import sys
import os

# ✅ FIX PROJECT ROOT PATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

# ✅ SAFE IMPORTS (with fallback debug)
try:
    from scripts.ingest import main as run_ingest
    from scripts.transform import main as run_transform
    PIPELINE_AVAILABLE = True
except Exception as e:
    st.error(f"Import error: {e}")
    PIPELINE_AVAILABLE = False


# Page config
st.set_page_config(page_title="Weather Dashboard")

st.title("🌦️ Live Weather Dashboard")
st.write("Real-time weather data powered by OpenWeather API")


# ✅ RUN PIPELINE ONLY IF IMPORT WORKS
if PIPELINE_AVAILABLE:
    try:
        if "pipeline_ran" not in st.session_state:
            run_ingest()
            run_transform()
            st.session_state.pipeline_ran = True
    except Exception as e:
        st.error(f"Pipeline failed: {e}")
else:
    st.warning("Pipeline modules not available")


# ✅ LOAD DATA
DATA_PATH = os.path.join(ROOT_DIR, "data", "transformed_weather.csv")

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("No data found. Pipeline not generating data.")
    st.stop()


# ✅ PROCESS DATA
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    df = df.drop_duplicates(subset="city")

if "temperature_c" in df.columns:
    df["temperature_c"] = df["temperature_c"].round(2)


# ✅ SHOW UPDATED TIME
if not df.empty:
    st.caption(f"Last updated: {df['timestamp'].iloc[0]}")


# ✅ CLEAN DISPLAY
df_display = df.rename(columns={
    "city": "City",
    "temperature": "Temperature (K)",
    "temperature_c": "Temperature (°C)",
    "timestamp": "Last Updated"
})


# ✅ TABLE
st.subheader("Latest Weather Data")
st.dataframe(df_display)


# ✅ CHART
st.subheader("Temperature (°C)")

if len(df_display) > 0:
    st.bar_chart(df_display.set_index("City")["Temperature (°C)"])
else:
    st.warning("No data available.")


# ✅ FOOTER
st.markdown("---")
st.caption("Built by Christal Haines 🚀")
