import streamlit as st
from utils import get_bq_client
import pandas as pd
from datetime import date

def app():
    st.title("🗓️ Book an Appointment")
    
    client = get_bq_client()
    
    # Select specialist
    query_specialists = "SELECT name, specialty FROM `medical-booking-system-473907.MedicalBookingDB.Specialists`"
    specialists = client.query(query_specialists).to_dataframe()
    
    specialist = st.selectbox("Select Specialist", specialists["name"])
    
    # Select date
    appointment_date = st.date_input("Select Date", min_value=date.today())
    
    # Select time slot (mock)
    time_slots = ["09:00", "10:00", "11:00", "14:00", "15:00"]
    time_slot = st.selectbox("Select Time Slot", time_slots)
    
    # User info
    patient_name = st.text_input("Your Name")
    patient_email = st.text_input("Your Email")
    
    if st.button("Book Appointment"):
        st.success(f"✅ Appointment booked with {specialist} on {appointment_date} at {time_slot}")
        # Optional: Insert booking into BigQuery
        # client.query(f"INSERT INTO ... VALUES (...)")

