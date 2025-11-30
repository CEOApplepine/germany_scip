import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.title("📦 Supply Chain Analytics")

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

# --- Clean columns ---
df.columns = df.columns.str.lower().str.replace(" ", "_")

# --- Required columns check ---
required_cols = ["supplier_id", "product_id", "planned_arrival", "actual_arrival", "lead_time_hours", "quantity"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    st.stop()

# --- Convert dates ---
df["planned_arrival"] = pd.to_datetime(df["planned_arrival"], errors="coerce")
df["actual_arrival"] = pd.to_datetime(df["actual_arrival"], errors="coerce")

# --- Lead time trend chart ---
st.subheader("📈 Lead Time Trend")
lead_time_trend = df.groupby("planned_arrival")["lead_time_hours"].mean().reset_index()
fig1 = px.line(lead_time_trend, x="planned_arrival", y="lead_time_hours", title="Average Lead Time Over Time")
st.plotly_chart(fig1, use_container_width=True)

# --- Supplier Performance ---
st.subheader("🏭 Supplier Lead Time Performance")
supplier_summary = df.groupby("supplier_id")["lead_time_hours"].mean().sort_values()
fig2 = px.bar(supplier_summary, x=supplier_summary.index, y="lead_time_hours", labels={"x":"Supplier ID", "lead_time_hours":"Avg Lead Time (hrs)"})
st.plotly_chart(fig2, use_container_width=True)

# --- Product Performance ---
st.subheader("📦 Product Lead Time Performance")
product_summary = df.groupby("product_id")["lead_time_hours"].mean().sort_values()
fig3 = px.bar(product_summary, x=product_summary.index, y="lead_time_hours", labels={"x":"Product ID", "lead_time_hours":"Avg Lead Time (hrs)"})
st.plotly_chart(fig3, use_container_width=True)

# --- Full dataset ---
st.subheader("📄 Full Delivery Data")
st.dataframe(df)
