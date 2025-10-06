import streamlit as st
from utils import get_specialists, book_appointment, client
import pandas as pd

def app():
    st.header("📅 Book an Appointment")

    # Load specialists
    specialists_df = get_specialists()
    specialist_options = specialists_df["name"].tolist()
    specialist_name = st.selectbox("Select Specialist", specialist_options)
    selected = specialists_df[specialists_df["name"]==specialist_name].iloc[0]

    st.write(f"**Specialty:** {selected.specialty}")
    st.write(f"**Average Rating:** {selected.avg_rating:.1f} ⭐ ({selected.num_feedback} reviews)")

    # Booking inputs
    patient_id = st.text_input("Enter your Patient ID")
    start_time = st.date_input("Select Date") 
    start_hour = st.number_input("Start Hour (24h)", min_value=0, max_value=23, value=9)
    start_minute = st.number_input("Start Minute", min_value=0, max_value=59, value=0)
    duration = st.number_input("Duration (minutes)", min_value=15, max_value=120, value=30)
    notes = st.text_area("Notes / Reason for Visit")

    if st.button("Book Appointment"):
        start_timestamp = f"{start_time} {start_hour}:{start_minute}:00"
        end_timestamp = f"{start_time} {start_hour}:{start_minute + duration}:00"
        book_appointment(selected.specialist_id, patient_id, start_timestamp, end_timestamp, notes)
        st.success("✅ Appointment booked successfully!")
