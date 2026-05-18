CITY = "Johannesburg"
DB_NAME = "data.db"

try:
    import streamlit as st
    API_KEY = st.secrets["API_KEY"]   # for deployed app
except:
    API_KEY = "your_local_api_key_here"   # for local testing
