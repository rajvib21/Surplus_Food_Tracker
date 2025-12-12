import streamlit as st
from db import get_conn

def admin_dashboard():
    st.title("Admin Dashboard")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    st.metric("Total Users", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM donations")
    st.metric("Total Donations", cur.fetchone()[0])

    cur.execute("SELECT SUM(quantity) FROM donations")
    st.metric("Total Quantity Donated", cur.fetchone()[0] or 0)

    cur.execute("SELECT SUM(saved_kg) FROM stats")
    st.metric("Total Waste Saved (kg)", cur.fetchone()[0] or 0)

    st.subheader("All Donations")
    cur.execute("SELECT * FROM donations")
    rows = cur.fetchall()
    for d in rows:
        st.write(dict(d))

    conn.close()
