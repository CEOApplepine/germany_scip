# dashboard_streamlit/pages/02_Procurement.py
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Procurement", layout="wide")
st.title("Procurement & Spend Analysis")

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
    st.warning("deliveries_curated.csv not found or is empty in data/.")
    st.stop()

# detect cost column
cost_candidates = ['cost', 'cost_eur', 'amount', 'price', 'total', 'spend']
cost_col = next((c for c in cost_candidates if c in df.columns), None)
supplier_col = next((c for c in ['supplier','supplier_name','vendor'] if c in df.columns), None)
category_col = next((c for c in ['category','product_category'] if c in df.columns), None)
date_col = next((c for c in ['date','ds'] if c in df.columns), None)

if cost_col is None:
    st.info("No cost column found in data; procurement spend charts require a numeric cost column.")
else:
    st.write(f"Using cost column: **{cost_col}**")

# Spend by supplier
if cost_col and supplier_col:
    spend = df.groupby(supplier_col)[cost_col].sum().reset_index().sort_values(cost_col, ascending=False)
    st.subheader("Total Spend by Supplier")
    fig = px.bar(spend, x=supplier_col, y=cost_col, title="Supplier Spend")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Supplier or cost column missing - cannot show spend by supplier.")

# Spend by category
if cost_col and category_col:
    spend_cat = df.groupby(category_col)[cost_col].sum().reset_index().sort_values(cost_col, ascending=False)
    st.subheader("Spend by Category")
    fig2 = px.pie(spend_cat, names=category_col, values=cost_col, title="Spend by Category")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Category or cost column missing - cannot show spend by category.")

# Monthly spend trend (if date present)
if cost_col and date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    monthly = df.groupby(pd.Grouper(key=date_col, freq='M'))[cost_col].sum().reset_index()
    st.subheader("Monthly Spend Trend")
    fig3 = px.line(monthly, x=date_col, y=cost_col, title="Monthly Spend")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Date or cost column missing - cannot show monthly trend.")
