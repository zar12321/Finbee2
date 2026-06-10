import streamlit as st


def open_chart_card(title):

    st.markdown(
        f"""
        <div class="chart-card">

            <div class="chart-header">

                <span class="chart-title">
                    {title}
                </span>

            </div>
        """,
        unsafe_allow_html=True
    )


def close_chart_card():

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )