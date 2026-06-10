import streamlit as st


def render_navbar(user_name):

    st.markdown(
        f"""
        <div class="navbar">

            <div class="navbar-left">

                <span class="navbar-logo">
                    🐝 FinBee
                </span>

            </div>

            <div class="navbar-right">

                <span class="navbar-user">
                    {user_name}
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )