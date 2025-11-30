import streamlit as st
import pandas as pd
import os

st.title("🚚 Supply Chain Performance")

# Load deliveries dataset
DATA_PATH = os.path.join("data", "deliveries_curated.csv")
df = pd.read_csv(DATA_PATH)

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Validate required columns
required_cols = [
    "date", "supplier_id", "product_id",
    "planned_arrival", "actual_arrival",
    "lead_time", "quantity"
]

missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    st.stop()

# Convert dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["planned_arrival"] = pd.to_datetime(df["planned_arrival"], errors="coerce")
df["actual_arrival"] = pd.to_datetime(df["actual_arrival"], errors="coerce")

# Create delay column
df["delay_days"] = (df["actual_arrival"] - df["planned_arrival"]).dt.days

# Create on-time flag
df["on_time"] = df["delay_days"] <= 0

# --------------------------
# KPI Metrics
# --------------------------
st.header("📊 Key Supply Chain Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Lead Time (days)", f"{df['lead_time'].mean():.1f}")
col2.metric("Average Delay (days)", f"{df['delay_days'].mean():.1f}")
col3.metric("On-Time Delivery Rate", f"{df['on_time'].mean() * 100:.1f}%")

# --------------------------
# Lead Time Trend
# --------------------------
st.subheader("📈 Lead Time Trend")

lead_time_trend = df.groupby("date")["lead_time"].mean()
st.line_chart(lead_time_trend)

# --------------------------
# Delivery Delay Trend
# --------------------------
st.subheader("⏱ Delay Trend (Planned vs Actual)")

delay_trend = df.groupby("date")["delay_days"].mean()
st.line_chart(delay_trend)

# --------------------------
# Supplier Performance
# --------------------------
st.subheader("🏭 Supplier Performance")

supplier_perf = df.groupby("supplier_id").agg({
    "lead_time": "mean",
    "delay_days": "mean",
    "on_time": "mean",
    "quantity": "sum"
}).rename(columns={
    "lead_time": "avg_lead_time",
    "delay_days": "avg_delay",
    "on_time": "on_time_rate",
    "quantity": "total_quantity"
})

st.dataframe(supplier_perf)

# --------------------------
# Product Performance
# --------------------------
st.subheader("📦 Product Performance")

product_perf = df.groupby("product_id").agg({
    "lead_time": "mean",
    "delay_days": "mean",
    "on_time": "mean",
    "quantity": "sum"
}).rename(columns={
    "lead_time": "avg_lead_time",
    "delay_days": "avg_delay",
    "on_time": "on_time_rate",
    "quantity": "total_quantity"
})

st.dataframe(product_perf)

# --------------------------
# Raw Data
# --------------------------
st.subheader("📄 Full Delivery Data")
st.dataframe(df)
