import streamlit as st

def render_navbar(user_name):

    st.markdown(
        f"""
        <div>
            <span>🐝 FinBee</span>
            <span>{user_name}</span>
        </div>
        """,
        unsafe_allow_html=True
    )