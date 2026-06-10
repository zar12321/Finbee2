import streamlit as st


def render_chart_card(title):

    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-header">
                <span class="chart-title">
                    {title}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )