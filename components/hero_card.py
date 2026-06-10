import streamlit as st

def render_hero_card(
    title,
    subtitle,
    user_name,
    emoji="🐝"
):

    st.error("TES HERO CARD")

    st.markdown(
        f"""
        <div class="hero-card">
            <h1>TES HERO CARD</h1>
        </div>
        """,
        unsafe_allow_html=True
    )