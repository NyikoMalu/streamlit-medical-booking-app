import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import json

@st.cache_resource
def get_bq_client():
    """
    Returns a cached BigQuery client using Streamlit secrets for authentication.
    """
    credentials_info = json.loads(st.secrets["bigquery"]["service_account"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = bigquery.Client(credentials=credentials, project=credentials_info["project_id"])
    return client

