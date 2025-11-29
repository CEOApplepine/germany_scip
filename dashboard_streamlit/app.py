
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SCIP Dashboard", layout="wide")
st.title("Germany Supply Chain Intelligence Platform (SCIP)")

deliveries = import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
deliveries_file = os.path.join(BASE_DIR, '..', 'data', 'deliveries_curated.csv')

deliveries = pd.read_csv(deliveries_file)
forecast = pd.read_csv('/content/germany-scip/data/forecast.csv')

st.header("Delivery Overview")
st.dataframe(deliveries)

st.header("Forecast Next 7 Days")
st.line_chart(forecast[['ds','yhat']])
