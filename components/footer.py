import streamlit as st

from config.settings import APP_VERSION


def render_footer():

    st.markdown(
        f"""
        <div class="footer">

            <span>
                FinBee Personal Finance Dashboard
            </span>

            <span>
                Version {APP_VERSION}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )