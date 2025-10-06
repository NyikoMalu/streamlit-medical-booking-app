import streamlit as st
from utils import client
import pandas as pd
import plotly.express as px

def app():
    st.header("📊 Admin Panel")
    password = st.text_input("Enter admin password", type="password")
    if password != "admin123":
        st.warning("Incorrect password!")
        return

    st.success("Access granted!")

    # Total bookings per day
    query = """
    SELECT DATE(start_time) AS date, COUNT(*) AS total_bookings
    FROM `bia-712-a2.MedicalBookingDB.appointments`
    GROUP BY date
    ORDER BY date
    """
    df = client.query(query).to_dataframe()
    fig = px.line(df, x="date", y="total_bookings", title="Bookings per Day")
    st.plotly_chart(fig)

    # Most popular specialists
    query2 = """
    SELECT s.name, COUNT(a.appointment_id) AS total_appointments
    FROM `bia-712-a2.MedicalBookingDB.specialists` s
    JOIN `bia-712-a2.MedicalBookingDB.appointments` a
      ON s.specialist_id = a.specialist_id
    GROUP BY s.name
    ORDER BY total_appointments DESC
    """
    df2 = client.query(query2).to_dataframe()
    fig2 = px.bar(df2, x="name", y="total_appointments", title="Most Popular Specialists")
    st.plotly_chart(fig2)

    # Average rating per specialist
    query3 = """
    SELECT s.name, IFNULL(AVG(f.rating),0) AS avg_rating
    FROM `bia-712-a2.MedicalBookingDB.specialists` s
    LEFT JOIN `bia-712-a2.MedicalBookingDB.appointments` a
      ON s.specialist_id = a.specialist_id
    LEFT JOIN `bia-712-a2.MedicalBookingDB.feedback` f
      ON a.appointment_id = f.appointment_id
    GROUP BY s.name
    ORDER BY avg_rating DESC
    """
    df3 = client.query(query3).to_dataframe()
    fig3 = px.scatter(df3, x="name", y="avg_rating", size="avg_rating", title="Average Ratings per Specialist")
    st.plotly_chart(fig3)
