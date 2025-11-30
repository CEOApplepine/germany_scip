import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📈 7-Day Forecast")

# --- Load data ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
forecast_file = os.path.join(BASE_DIR, "..", "data", "forecast.csv")

@st.cache_data
def load_data():
    return pd.read_csv(forecast_file)

try:
    forecast = load_data()
except FileNotFoundError:
    st.error("❌ forecast.csv not found in /data folder.")
    st.stop()

# --- Validate Columns ---
required_cols = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
missing = [c for c in required_cols if c not in forecast.columns]
if missing:
    st.error(f"Missing columns in forecast.csv: {missing}")
    st.stop()

# --- Convert date ---
forecast['ds'] = pd.to_datetime(forecast['ds'])

# --- Metrics ---
st.subheader("📊 Key Forecast Metrics")

col1, col2 = st.columns(2)
col1.metric("Average Expected Deliveries", f"{forecast['yhat'].mean():.0f}")
col2.metric("Max Forecasted Deliveries", f"{forecast['yhat'].max():.0f}")

# --- Forecast Line Chart ---
fig = px.line(
    forecast,
    x='ds',
    y=['yhat', 'yhat_lower', 'yhat_upper'],
    labels={'ds': 'Date', 'value': 'Forecast'},
    title='Delivery Forecast with Confidence Interval'
)
st.plotly_chart(fig, use_container_width=True)

# --- Table ---
st.subheader("📋 Forecast Data Table")
st.dataframe(forecast)
