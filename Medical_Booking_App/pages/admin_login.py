# pages/admin_login.py
import streamlit as st

def show():
    st.title("🔒 Admin Login")
    st.markdown("Only administrators can access the admin panel.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # validate against secrets
        try:
            admin_user = st.secrets["ADMIN"]["username"]
            admin_pass = st.secrets["ADMIN"]["password"]
        except Exception:
            st.error("Admin credentials not found in Streamlit secrets. Add ADMIN username/password.")
            return

        if username == admin_user and password == admin_pass:
            st.success("Login successful — redirecting to admin panel...")
            # show panel in-place
            from pages.admin_panel import show as admin_panel_show
            admin_panel_show()
        else:
            st.error("Invalid credentials.")
