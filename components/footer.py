import streamlit as st

from config.settings import APP_VERSION


def render_footer():
    st.markdown(
        """
        <div style="
            text-align:center;
            padding:20px;
            color:white;
        ">
            FinBee Footer
        </div>
        """,
        unsafe_allow_html=True
    )