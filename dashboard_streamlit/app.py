import streamlit as st
import pandas as pd

st.set_page_config(page_title="SCIP Dashboard", layout="wide")
st.title("Germany Supply Chain Intelligence Platform (SCIP)")

deliveries = pd.read_csv('/content/germany_scip/data/deliveries_curated.csv')
forecast = pd.read_csv('/content/germany_scip/data/forecast.csv')

st.header("Delivery Overview")
st.dataframe(deliveries)

st.header("Forecast Next 7 Days")
st.line_chart(forecast[['ds','yhat']])

