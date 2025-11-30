import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.title("📊 Overview Dashboard")

# --- Load deliveries dataset ---
DATA_PATH = os.path.join("data", "deliveries_curated.csv")
df = pd.read_csv(DATA_PATH)

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert dates
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# --------------------------
# Key Metrics
# --------------------------
st.header("📌 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Deliveries", len(df))
col2.metric("Unique Suppliers", df['supplier_id'].nunique())
col3.metric("Unique Products", df['product_id'].nunique())
col4.metric("Average Lead Time (days)", f"{df['lead_time'].mean():.1f}")
col5.metric("Average Cost (€)", f"{df['cost_eur'].mean():.2f}")

# --------------------------
# Daily Deliveries Trend
# --------------------------
st.subheader("📈 Daily Deliveries Trend")

daily_deliveries = df.groupby('date')['quantity'].sum().reset_index()
fig1 = px.line(daily_deliveries, x='date', y='quantity', title='Daily Deliveries')
st.plotly_chart(fig1, use_container_width=True)

# --------------------------
# Total Cost Trend
# --------------------------
st.subheader("💰 Total Cost Trend")

daily_cost = df.groupby('date')['cost_eur'].sum().reset_index()
fig2 = px.line(daily_cost, x='date', y='cost_eur', title='Total Cost per Day')
st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# Full Dataset
# --------------------------
st.subheader("📄 Full Deliveries Table")
st.dataframe(df)
