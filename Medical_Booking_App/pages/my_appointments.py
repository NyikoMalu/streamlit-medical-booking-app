import streamlit as st
from utils import get_bq_client
import pandas as pd

def app():
    st.title("📑 My Appointments")
    
    client = get_bq_client()
    
    patient_email = st.text_input("Enter your Email to see your bookings")
    
    if patient_email:
        query = f"""
            SELECT specialist_name, appointment_date, time_slot
            FROM `medical-booking-system-473907.MedicalBookingDB.Appointments`
            WHERE patient_email = '{patient_email}'
            ORDER BY appointment_date
        """
        df = client.query(query).to_dataframe()
        
        if not df.empty:
            st.write(f"Found {len(df)} appointments")
            st.dataframe(df)
            
            # Visualization: appointments over time
            df_grouped = df.groupby("appointment_date").size().reset_index(name="count")
            st.line_chart(df_grouped.rename(columns={"appointment_date": "index"}).set_index("index")["count"])
        else:
            st.info("No appointments found for this email.")
