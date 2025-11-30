import streamlit as st
import os
import pandas as pd

# --- Page config ---
st.set_page_config(
    page_title="Germany SCIP Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar navigation ---
st.sidebar.title("Germany SCIP Dashboard")
pages = {
    "🏠 Home": "home",
    "📊 Overview": "overview",
    "💰 Procurement": "procurement",
    "🚚 Supply Chain": "supply_chain",
    "📈 Forecasts": "forecast",
    "📝 NLP Insights": "nlp"
}

selection = st.sidebar.radio("Go to page:", list(pages.keys()))

# --- Paths ---
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

# --- Home page ---
if pages[selection] == "home":
    st.title("Germany Supply Chain Intelligence Platform — Home")
    st.header("Project Summary")
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
    col3.metric("Total rows", len(deliveries) if deliveries is not None else "N/A")
    st.markdown(
        "**Notes:** Make sure `data/deliveries_curated.csv` and `data/forecast.csv` exist in the repo root `data/` folder."
    )

# --- Load pages dynamically ---
else:
    try:
        if pages[selection] == "overview":
            from pages import _01_Overview as page
        elif pages[selection] == "procurement":
            from pages import _02_Procurement as page
        elif pages[selection] == "supply_chain":
            from pages import _03_SupplyChain as page
        elif pages[selection] == "forecast":
            from pages import _04_Forecast as page
        elif pages[selection] == "nlp":
            from pages import _05_NLP as page
        else:
            st.error("Page not found.")
            page = None

        if page:
            page.run()
    except Exception as e:
        st.error(f"❌ Failed to load page: {e}")
