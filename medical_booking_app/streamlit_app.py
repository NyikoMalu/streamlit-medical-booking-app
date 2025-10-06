import streamlit as st
from google.cloud import bigquery

# ----------------------
# BigQuery Client Setup
# ----------------------
# Authenticate using service account JSON
# export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account.json"
client = bigquery.Client(project="bia-712-a2")

st.set_page_config(page_title="Medical Booking System", layout="wide")
st.title("Medical Booking System")
st.sidebar.success("Select a page from above navigation")
