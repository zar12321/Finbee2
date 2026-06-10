import streamlit as st


import streamlit as st


def render_navbar(user_name):

    st.markdown(
        f"""
        <div>
            🐝 FinBee | {user_name}
        </div>
        """,
        unsafe_allow_html=True
    )