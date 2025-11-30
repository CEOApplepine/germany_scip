# dashboard_streamlit/app.py
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SCIP Dashboard - Home", layout="wide")
st.title("Germany Supply Chain Intelligence Platform — Home")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DELIVERIES_FILE = os.path.join(DATA_DIR, 'deliveries_curated.csv')
FORECAST_FILE = os.path.join(DATA_DIR, 'forecast.csv')

@st.cache_data
def load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        return None

deliveries = load_csv(DELIVERIES_FILE)
forecast = load_csv(FORECAST_FILE)

st.header("Project summary")
st.write(
    "This project provides delivery analytics, procurement insights, supply-chain trends, "
    "NLP analysis of textual feedback, and short-term forecasts. Use the pages in the sidebar "
    "to explore: Overview, Procurement, Supply Chain, NLP, and Forecasts."
)

st.markdown("---")
st.header("Quick snapshot")

col1, col2, col3 = st.columns(3)
col1.metric("Deliveries file", "Loaded" if deliveries is not None else "Missing")
col2.metric("Forecast file", "Loaded" if forecast is not None else "Missing")
if deliveries is not None:
    col3.metric("Total rows", len(deliveries))
else:
    col3.metric("Total rows", "N/A")

st.markdown("**Notes:** Make sure `data/deliveries_curated.csv` and `data/forecast.csv` exist in the repo root `data/` folder.")
