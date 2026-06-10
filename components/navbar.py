import streamlit as st


import streamlit as st

def render_navbar(user_name):

    st.markdown(
        f"""
        <div class="navbar">
            <div class="navbar-left">
                🐝 FinBee
            </div>

            <div class="navbar-right">
                {user_name}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )