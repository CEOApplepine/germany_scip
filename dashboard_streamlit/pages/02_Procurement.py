import streamlit as st
import pandas as pd
import os

st.title("💰 Procurement Analytics")

# Load data
DATA_PATH = os.path.join("data", "deliveries_curated.csv")
df = pd.read_csv(DATA_PATH)

# Rename columns to clean names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Check for required columns
required = ["supplier_id", "product_id", "cost_eur"]
missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"❌ Missing columns: {', '.join(missing)}")
    st.stop()

# Convert cost to numeric
df["cost_eur"] = pd.to_numeric(df["cost_eur"], errors="coerce").fillna(0)

# --------------------------
# Spend by Supplier
# --------------------------
st.header("📦 Spend by Supplier")

spend_supplier = df.groupby("supplier_id")["cost_eur"].sum().sort_values(ascending=False)
st.bar_chart(spend_supplier)

# --------------------------
# Spend by Product
# --------------------------
st.header("🏷 Spend by Product")

spend_product = df.groupby("product_id")["cost_eur"].sum().sort_values(ascending=False)
st.bar_chart(spend_product)

# --------------------------
# Summary Metrics
# --------------------------
st.header("📊 Procurement KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Spend (€)", f"{df['cost_eur'].sum():,.0f}")
col2.metric("Unique Suppliers", df["supplier_id"].nunique())
col3.metric("Unique Products", df["product_id"].nunique())

# --------------------------
# Full Dataset View
# --------------------------
st.header("📄 Procurement Data Table")
st.dataframe(df)
