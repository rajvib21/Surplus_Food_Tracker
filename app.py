import streamlit as st
from auth import login, register
from db import init_db
from admin_panel import admin_dashboard
from user_panel import user_dashboard
from chatbot import ask_ollama

init_db()
st.sidebar.title("Surplus Food Tracker")

page = st.sidebar.selectbox("Menu", ["Login", "Register", "Chatbot"])

if page == "Login":
    st.title("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        logged = login(user, pwd)
        if logged:
            st.session_state["user"] = logged
            st.success("Logged in!")

    if "user" in st.session_state:
        if st.session_state["user"]["role"] == "admin":
            admin_dashboard()
        else:
            user_dashboard(st.session_state["user"])

elif page == "Register":
    st.title("Register")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if register(user, pwd):
            st.success("Registered successfully!")
        else:
            st.error("Username already exists.")

elif page == "Chatbot":
    st.title("AI Chatbot (Ollama Local LLM)")
    prompt = st.text_area("Ask anything!")
    if st.button("Send"):
        reply = ask_ollama(prompt)
        st.write(reply)
