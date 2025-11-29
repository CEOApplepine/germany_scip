# dashboard_streamlit/app.py

import os
import pandas as pd
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="SCIP Dashboard", layout="wide")
st.title("Germany Supply Chain Intelligence Platform (SCIP)")

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
deliveries_file = os.path.join(DATA_DIR, 'deliveries_curated.csv')
forecast_file = os.path.join(DATA_DIR, 'forecast.csv')  # ensure this file exists

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return pd.DataFrame()  # return empty DataFrame

deliveries = load_csv(deliveries_file)
forecast = load_csv(forecast_file)

# -----------------------------
# Display Delivery Overview
# -----------------------------
st.header("Delivery Overview")
if deliveries.empty:
    st.warning("No deliveries data available. Check data folder.")
else:
    st.dataframe(deliveries)

# -----------------------------
# Display Forecast Next 7 Days
# -----------------------------
st.header("Forecast Next 7 Days")
if forecast.empty:
    st.warning("No forecast data available. Check data folder.")
else:
    # Ensure 'ds' and 'yhat' columns exist
    if all(col in forecast.columns for col in ['ds','yhat']):
        st.line_chart(forecast[['ds','yhat']])
    else:
        st.error("Forecast CSV must contain 'ds' and 'yhat' columns")
