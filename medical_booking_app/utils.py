from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client(project="bia-712-a2")

# Fetch all specialists with average rating
def get_specialists():
    query = """
    SELECT s.specialist_id, s.name, s.specialty, s.contact_email, s.phone,
           s.bio, s.photo_url,
           IFNULL(AVG(f.rating), 0) AS avg_rating,
           COUNT(f.feedback_id) AS num_feedback
    FROM `bia-712-a2.MedicalBookingDB.specialists` s
    LEFT JOIN `bia-712-a2.MedicalBookingDB.appointments` a
           ON s.specialist_id = a.specialist_id
    LEFT JOIN `bia-712-a2.MedicalBookingDB.feedback` f
           ON a.appointment_id = f.appointment_id
    GROUP BY s.specialist_id, s.name, s.specialty, s.contact_email, s.phone, s.bio, s.photo_url
    ORDER BY avg_rating DESC
    """
    df = client.query(query).to_dataframe()
    return df

# Fetch appointments for a specialist
def get_appointments(specialist_id):
    query = f"""
    SELECT a.appointment_id, p.full_name AS patient_name, a.start_time, a.end_time, a.status, a.notes
    FROM `bia-712-a2.MedicalBookingDB.appointments` a
    JOIN `bia-712-a2.MedicalBookingDB.patients` p
      ON a.patient_id = p.patient_id
    WHERE a.specialist_id = '{specialist_id}'
    ORDER BY a.start_time
    """
    return client.query(query).to_dataframe()

# Book a new appointment
def book_appointment(specialist_id, patient_id, start_time, end_time, notes):
    query = f"""
    INSERT INTO `bia-712-a2.MedicalBookingDB.appointments`
    (appointment_id, specialist_id, patient_id, start_time, end_time, status, notes, created_at, updated_at)
    VALUES
    (GENERATE_UUID(), '{specialist_id}', '{patient_id}', TIMESTAMP('{start_time}'),
     TIMESTAMP('{end_time}'), 'booked', '{notes}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
    """
    client.query(query)
    return True
