import streamlit as st
from streamlit_option_menu import option_menu

# --- Sidebar Navigation ---
with st.sidebar:
    selected = option_menu(
        "📋 Navigation",
        ["🏠 Home", "👨‍⚕️ Specialists", "🗓️ Book Appointment", "📑 My Appointments"],
        icons=["house", "person-badge", "calendar-plus", "journal-text"],
        menu_icon="cast",
        default_index=0,
    )

# --- Page routing ---
if selected == "🏠 Home":
    from pages.home import app as home_app
    home_app()
elif selected == "👨‍⚕️ Specialists":
    from pages.specialists import app as specialists_app
    specialists_app()
elif selected == "🗓️ Book Appointment":
    from pages.book_appointment import app as book_app
    book_app()
elif selected == "📑 My Appointments":
    from pages.my_appointments import app as my_appointments_app
    my_appointments_app()

