import streamlit as st
from utils import get_specialists

def app():
    st.header("🩺 Specialist Profiles")
    specialists_df = get_specialists()

    for _, row in specialists_df.iterrows():
        st.subheader(row["name"])
        st.write(f"**Specialty:** {row['specialty']}")
        st.write(f"**Email:** {row['contact_email']}")
        st.write(f"**Phone:** {row['phone']}")
        st.write(f"**Average Rating:** {row['avg_rating']:.1f} ⭐ ({row['num_feedback']} reviews)")
        if row["bio"]:
            st.write(f"**Bio:** {row['bio']}")
        st.write("---")

