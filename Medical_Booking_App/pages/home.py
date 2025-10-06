import streamlit as st
import plotly.express as px
from utils import get_bq_client
import pandas as pd

def app():
    st.title("🏥 Medical Booking System Dashboard")
    st.write("Welcome! Use the sidebar to navigate to different pages.")

    client = get_bq_client()

    # --- Filters ---
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    # --- Appointments Trend (Line Chart) ---
    query = f"""
        SELECT appointment_date, COUNT(*) AS total
        FROM `medical-booking-system-473907.MedicalBookingDB.Appointments`
        WHERE appointment_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY appointment_date
        ORDER BY appointment_date
    """
    df = client.query(query).to_dataframe()

    if not df.empty:
        st.subheader("📈 Appointments Over Time")
        fig_line = px.line(df, x="appointment_date", y="total",
                           markers=True, title="Appointments Over Time",
                           labels={"appointment_date": "Date", "total": "Appointments"})
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("ℹ️ No appointment data for this period.")

    # --- Top Specialties (Bar Chart) ---
    query2 = """
        SELECT specialty, COUNT(*) AS total
        FROM `medical-booking-system-473907.MedicalBookingDB.Specialists`
        GROUP BY specialty
        ORDER BY total DESC
        LIMIT 10
    """
    df2 = client.query(query2).to_dataframe()

    if not df2.empty:
        st.subheader("🏆 Top Specialties")
        fig_bar = px.bar(df2, x="specialty", y="total", text="total",
                         title="Specialists by Specialty", color="specialty")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Ratings Scatter Plot ---
    query3 = """
        SELECT name, specialty, rating
        FROM `medical-booking-system-473907.MedicalBookingDB.Specialists`
        WHERE rating IS NOT NULL
        ORDER BY rating DESC
        LIMIT 50
    """
    df3 = client.query(query3).to_dataframe()

    if not df3.empty:
        st.subheader("⭐ Specialist Ratings")
        fig_scatter = px.scatter(df3, x="specialty", y="rating", size="rating", color="specialty",
                                 hover_data=["name"], title="Specialist Ratings by Specialty")
        st.plotly_chart(fig_scatter, use_container_width=True)


