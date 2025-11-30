# dashboard_streamlit/app.py

import os
import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="SCIP Dashboard", layout="wide")
st.title("Germany Supply Chain Intelligence Platform (SCIP)")

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

deliveries_file = os.path.join(DATA_DIR, 'deliveries_curated.csv')
forecast_file = os.path.join(DATA_DIR, 'forecast.csv')

# -----------------------------
# Load data with caching
# -----------------------------
@st.cache_data
def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return pd.DataFrame()

deliveries = load_csv(deliveries_file)
forecast = load_csv(forecast_file)

# -----------------------------
# Delivery Overview Section
# -----------------------------
st.header("📦 Delivery Overview")

if not deliveries.empty:
    # KPI metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Deliveries", len(deliveries))
    col2.metric("Unique Products", deliveries['product'].nunique())
    col3.metric("Unique Suppliers", deliveries['supplier'].nunique())

    # Bar chart: Deliveries per Supplier
    deliveries_supplier = deliveries.groupby('supplier').size().reset_index(name='count')
    fig1 = px.bar(deliveries_supplier, x='supplier', y='count', title="Deliveries per Supplier")
    st.plotly_chart(fig1, use_container_width=True)

    # Bar chart: Deliveries per Product
    deliveries_product = deliveries.groupby('product').size().reset_index(name='count')
    fig2 = px.bar(deliveries_product, x='product', y='count', title="Deliveries per Product")
    st.plotly_chart(fig2, use_container_width=True)

    # Full deliveries table
    st.subheader("Full Deliveries Table")
    st.dataframe(deliveries)
else:
    st.warning("No deliveries data available.")

# -----------------------------
# Forecast Section
# -----------------------------
st.header("📈 Forecast Next 7 Days")

if not forecast.empty:
    if all(col in forecast.columns for col in ['ds','yhat']):
        fig3 = px.line(forecast, x='ds', y='yhat', title="7-Day Delivery Forecast", markers=True)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.error("Forecast CSV must contain 'ds' and 'yhat' columns")
else:
    st.warning("No forecast data available.")
