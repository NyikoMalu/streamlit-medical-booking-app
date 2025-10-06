# pages/admin_panel.py
import streamlit as st
from utils import get_bq_client, bq_to_df
import plotly.express as px
import pandas as pd

def show():
    st.title("⚙️ Admin Panel")
    st.markdown("Analytics, reports, and management tools for administrators.")

    client = get_bq_client()

    # KPI row
    try:
        q_kpis = """
        SELECT
          COUNT(DISTINCT SpecialistID) AS specialists,
          COUNT(DISTINCT PatientID) AS patients,
          COUNT(AppointmentID) AS appointments
        FROM `medical-booking-system-473907.MedicalBookingDB.Appointments`
        """
        kpi_df = bq_to_df(client, q_kpis)
        if not kpi_df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Specialists", kpi_df['specialists'].iloc[0])
            col2.metric("Patients", kpi_df['patients'].iloc[0])
            col3.metric("Appointments", kpi_df['appointments'].iloc[0])
    except Exception as e:
        st.error(f"KPI load error: {e}")

    st.divider()

    # Chart 1: Appointments over time (line) - already in home but admin version with date range
    st.subheader("Appointments Over Time (Admin)")
    min_date, max_date = st.date_input("Date range", [])
    # If no date range selected, query full
    date_filter = ""
    # For brevity show full trend
    q1 = """
    SELECT d.Date AS appointment_date, COUNT(a.AppointmentID) AS total
    FROM `medical-booking-system-473907.MedicalBookingDB.Appointments` a
    JOIN `medical-booking-system-473907.MedicalBookingDB.Dates` d ON a.DateKey = d.DateKey
    GROUP BY d.Date
    ORDER BY d.Date
    """
    df1 = bq_to_df(client, q1)
    if not df1.empty:
        df1['appointment_date'] = df1['appointment_date'].astype(str)
        fig1 = px.line(df1, x='appointment_date', y='total', title="Appointments Over Time", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # Chart 2: Top specialists by bookings (bar)
    st.subheader("Top Specialists by Bookings")
    q2 = """
    SELECT s.FirstName || ' ' || s.LastName AS SpecialistName, COUNT(*) AS bookings
    FROM `medical-booking-system-473907.MedicalBookingDB.Appointments` a
    JOIN `medical-booking-system-473907.MedicalBookingDB.Specialists` s ON a.SpecialistID = s.SpecialistID
    GROUP BY SpecialistName
    ORDER BY bookings DESC
    LIMIT 20
    """
    df2 = bq_to_df(client, q2)
    if not df2.empty:
        fig2 = px.bar(df2, x='SpecialistName', y='bookings', title="Most Booked Specialists")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Chart 3: Appointments by weekday/time (scatter / heatmap)
    st.subheader("Appointments by Weekday and Time Slot")
    q3 = """
    SELECT d.Weekday, t.Label AS TimeSlot, COUNT(*) AS total
    FROM `medical-booking-system-473907.MedicalBookingDB.Appointments` a
    JOIN `medical-booking-system-473907.MedicalBookingDB.Dates` d ON a.DateKey = d.DateKey
    JOIN `medical-booking-system-473907.MedicalBookingDB.TimeSlots` t ON a.TimeSlotID = t.TimeSlotID
    GROUP BY d.Weekday, TimeSlot
    ORDER BY d.Weekday
    """
    df3 = bq_to_df(client, q3)
    if not df3.empty:
        # create heatmap pivot
        pivot = df3.pivot(index='Weekday', columns='TimeSlot', values='total').fillna(0)
        st.write("Heatmap (weekday × timeslot)")
        fig3 = px.imshow(pivot, text_auto=True, aspect="auto", title="Appointments Heatmap")
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Admin export: download bookings CSV
    st.subheader("Export Booking Data")
    export_q = """
    SELECT a.AppointmentID, p.FirstName || ' ' || p.LastName AS Patient, s.FirstName || ' ' || s.LastName AS Specialist,
           d.Date AS Date, t.Label AS TimeSlot, a.Status
    FROM `medical-booking-system-473907.MedicalBookingDB.Appointments` a
    JOIN `medical-booking-system-473907.MedicalBookingDB.Patients` p ON a.PatientID = p.PatientID
    JOIN `medical-booking-system-473907.MedicalBookingDB.Specialists` s ON a.SpecialistID = s.SpecialistID
    JOIN `medical-booking-system-473907.MedicalBookingDB.Dates` d ON a.DateKey = d.DateKey
    JOIN `medical-booking-system-473907.MedicalBookingDB.TimeSlots` t ON a.TimeSlotID = t.TimeSlotID
    """
    df_export = bq_to_df(client, export_q)
    if not df_export.empty:
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("Download bookings as CSV", data=csv, file_name="bookings_export.csv", mime="text/csv")
