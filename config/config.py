CITY = "Johannesburg"
DB_NAME = "data.db"

try:
    import streamlit as st
    API_KEY = st.secrets["API_KEY"]   # for deployed app
except:
    API_KEY = "aba0eaf1dcafa9324bec8b8e81ca7ad3"   # for local testing
