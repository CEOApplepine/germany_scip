
# dashboard_streamlit/pages/01_Overview.py
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Overview", layout="wide")
st.title("Overview — Deliveries & KPIs")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')
DELIVERIES_FILE = os.path.join(DATA_DIR, 'deliveries_curated.csv')

@st.cache_data
def load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

df = load_csv(DELIVERIES_FILE)

if df.empty:
    st.warning("deliveries_curated.csv not found or is empty in data/ folder.")
    st.stop()

# helper to find supplier/product column names
def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

supplier_col = find_column(df, ['supplier', 'supplier_name', 'vendor'])
product_col = find_column(df, ['product', 'product_name', 'sku', 'item'])
date_col = find_column(df, ['date', 'ds', 'datetime', 'planned_date'])

# Basic KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Deliveries", len(df))
col2.metric("Unique Products", df[product_col].nunique() if product_col else "N/A")
col3.metric("Unique Suppliers", df[supplier_col].nunique() if supplier_col else "N/A")

st.markdown("---")
# Filters
with st.expander("Filters"):
    sel_supplier = None
    sel_product = None
    if supplier_col:
        suppliers = sorted(df[supplier_col].dropna().unique().tolist())
        sel_supplier = st.multiselect("Filter by supplier", suppliers, default=suppliers[:5])
    if product_col:
        products = sorted(df[product_col].dropna().unique().tolist())
        sel_product = st.multiselect("Filter by product", products, default=products[:10])

filtered = df.copy()
if supplier_col and sel_supplier:
    filtered = filtered[filtered[supplier_col].isin(sel_supplier)]
if product_col and sel_product:
    filtered = filtered[filtered[product_col].isin(sel_product)]

# Charts
st.subheader("Deliveries by Supplier")
if supplier_col:
    agg = filtered.groupby(supplier_col).size().reset_index(name='count').sort_values('count', ascending=False)
    fig = px.bar(agg, x=supplier_col, y='count', title="Deliveries per Supplier")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No supplier column found to show supplier chart.")

st.subheader("Deliveries by Product")
if product_col:
    agg2 = filtered.groupby(product_col).size().reset_index(name='count').sort_values('count', ascending=False)
    fig2 = px.bar(agg2, x=product_col, y='count', title="Deliveries per Product")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No product column found to show product chart.")

st.subheader("Deliveries Table")
st.dataframe(filtered)
