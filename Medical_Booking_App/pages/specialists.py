import streamlit as st
from utils import get_bq_client
import pandas as pd
import plotly.express as px

def app():
    st.title("👨‍⚕️ Specialists Directory")
    
    client = get_bq_client()
    
    # Filter by specialty
    query_specialties = "SELECT DISTINCT specialty FROM `medical-booking-system-473907.MedicalBookingDB.Specialists`"
    specialties = client.query(query_specialties).to_dataframe()["specialty"].tolist()
    
    selected_specialty = st.selectbox("Filter by Specialty", ["All"] + specialties)
    
    # Query specialists
    if selected_specialty == "All":
        query = "SELECT name, specialty, contact_info, rating FROM `medical-booking-system-473907.MedicalBookingDB.Specialists`"
    else:
        query = f"SELECT name, specialty, contact_info, rating FROM `medical-booking-system-473907.MedicalBookingDB.Specialists` WHERE specialty='{selected_specialty}'"
    
    df = client.query(query).to_dataframe()
    
    if not df.empty:
        st.write(f"Displaying {len(df)} specialists")
        st.dataframe(df)
        
        # Visual: ratings per specialty
        fig = px.bar(df, x="name", y="rating", color="rating",
                     hover_data=["specialty", "contact_info"], title="Specialist Ratings")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No specialists found for this selection.")
