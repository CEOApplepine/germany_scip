import streamlit as st
import pandas as pd
import os

st.title("📊 Overview")

# --- Load CSV robustly ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "deliveries_curated.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

try:
    df = pd.read_csv(DATA_PATH)
    st.success(f"✅ Deliveries CSV loaded successfully from {DATA_PATH}")
except FileNotFoundError:
    st.error(f"❌ File not found at: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading CSV: {e}")
    st.stop()

# --- Clean column names ---
df.columns = df.columns.str.lower().str.replace(" ", "_")

# --- Required columns check ---
required_cols = [
    "supplier_id", "product_id", "planned_arrival", "actual_arrival",
    "lead_time_hours", "cost_eur", "quantity"
]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    st.stop()

# --- Convert dates ---
df["planned_arrival"] = pd.to_datetime(df["planned_arrival"], errors="coerce")
df["actual_arrival"] = pd.to_datetime(df["actual_arrival"], errors="coerce")

# --- Compute delay and on-time ---
df["delay_hours"] = (df["actual_arrival"] - df["planned_arrival"]).dt.total_seconds() / 3600
df["on_time"] = df["delay_hours"] <= 0

# --- KPIs ---
st.header("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Deliveries", len(df))
col2.metric("Unique Products", df['product_id'].nunique())
col3.metric("Unique Suppliers", df['supplier_id'].nunique())
col4.metric("Average Lead Time (hours)", f"{df['lead_time_hours'].mean():.1f}")

# --- Lead Time Trend ---
st.subheader("📈 Lead Time Trend")
st.line_chart(df.groupby("planned_arrival")["lead_time_hours"].mean())

# --- Delivery Delay Trend ---
st.subheader("⏱ Delivery Delay Trend")
st.line_chart(df.groupby("planned_arrival")["delay_hours"].mean())

# --- Top Suppliers Table ---
st.subheader("🏭 Top Suppliers")
supplier_summary = df.groupby("supplier_id").agg({
    "lead_time_hours": "mean",
    "delay_hours": "mean",
    "on_time": "mean",
    "quantity": "sum",
    "cost_eur": "sum"
}).rename(columns={
    "lead_time_hours": "avg_lead_time_hours",
    "delay_hours": "avg_delay_hours",
    "on_time": "on_time_rate",
    "quantity": "total_quantity",
    "cost_eur": "total_cost_eur"
}).sort_values(by="avg_delay_hours", ascending=True)
st.dataframe(supplier_summary)

# --- Top Products Table ---
st.subheader("📦 Top Products")
product_summary = df.groupby("product_id").agg({
    "lead_time_hours": "mean",
    "delay_hours": "mean",
    "on_time": "mean",
    "quantity": "sum",
    "cost_eur": "sum"
}).rename(columns={
    "lead_time_hours": "avg_lead_time_hours",
    "delay_hours": "avg_delay_hours",
    "on_time": "on_time_rate",
    "quantity": "total_quantity",
    "cost_eur": "total_cost_eur"
}).sort_values(by="total_quantity", ascending=False)
st.dataframe(product_summary)

# --- Full Dataset ---
st.subheader("📄 Full Delivery Data")
st.dataframe(df)
